import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from conexion.conexion import obtener_conexion
from models import Usuario
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from forms.login_form import LoginForm
from forms.usuario_form import RegistroForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave_secreta_semana_15_desarrollo_web')

# --- CONFIGURACIÓN DE FLASK-LOGIN ---
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta sección.'
login_manager.login_message_category = 'warning'


@login_manager.user_loader
def load_user(user_id):
    conn = obtener_conexion()
    if conn is None:
        return None
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT id_usuario, usuario, email FROM usuarios WHERE id_usuario = %s', (user_id,))
    res = cursor.fetchone()
    cursor.close()
    conn.close()
    if res:
        return Usuario(res['id_usuario'], res['usuario'], res['email'])
    return None


# --- INICIALIZACIÓN DE LA BASE DE DATOS ---

def inicializar_base_datos():
    conn = None
    try:
        conn = obtener_conexion()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario SERIAL PRIMARY KEY,
                usuario VARCHAR(50) NOT NULL UNIQUE,
                email VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS proveedores (
                id_proveedor SERIAL PRIMARY KEY,
                empresa VARCHAR(100) NOT NULL,
                contacto VARCHAR(100) NOT NULL,
                telefono VARCHAR(20) NOT NULL,
                ciudad VARCHAR(50) NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id_producto SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                precio DECIMAL(10,2) NOT NULL,
                stock INT NOT NULL,
                categoria VARCHAR(50) NOT NULL,
                descripcion TEXT,
                id_proveedor INT,
                FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor) ON DELETE SET NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id_cliente SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                telefono VARCHAR(20) NOT NULL,
                estado VARCHAR(20) NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS facturas (
                id_factura SERIAL PRIMARY KEY,
                numero VARCHAR(20) NOT NULL,
                id_cliente INT,
                fecha DATE NOT NULL,
                total DECIMAL(10,2) NOT NULL,
                estado VARCHAR(20) NOT NULL,
                FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detalle_factura (
                id_detalle SERIAL PRIMARY KEY,
                id_factura INT NOT NULL,
                id_producto INT NOT NULL,
                cantidad INT NOT NULL,
                precio_unitario DECIMAL(10,2) NOT NULL,
                subtotal DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (id_factura) REFERENCES facturas(id_factura) ON DELETE CASCADE,
                FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
            )
        ''')
        conn.commit()

        cursor.execute('SELECT COUNT(*) AS total FROM usuarios')
        res_usr = cursor.fetchone()
        if res_usr and res_usr['total'] == 0:
            pass_hash = generate_password_hash('admin123')
            cursor.execute('''
                INSERT INTO usuarios (usuario, email, password)
                VALUES (%s, %s, %s)
            ''', ('admin', 'admin@brilla.com', pass_hash))
            conn.commit()

        cursor.execute('SELECT COUNT(*) AS total FROM proveedores')
        res_prov = cursor.fetchone()
        if res_prov and res_prov['total'] == 0:
            proveedores_iniciales = [
                ("Distribuidora Belleza S.A.", "Carlos Ruiz", "022345678", "Quito")
            ]
            cursor.executemany('''
                INSERT INTO proveedores (empresa, contacto, telefono, ciudad)
                VALUES (%s, %s, %s, %s)
            ''', proveedores_iniciales)
            conn.commit()

        cursor.execute('SELECT id_proveedor FROM proveedores ORDER BY id_proveedor LIMIT 1')
        prov_default = cursor.fetchone()
        id_prov = prov_default['id_proveedor'] if prov_default else None

        cursor.execute('SELECT COUNT(*) AS total FROM productos')
        resultado = cursor.fetchone()
        if resultado and resultado['total'] == 0:
            productos_iniciales = [
                ("Labial Matte Cream", 6.50, 12, "Labios", "Brinda color intenso de larga duración con textura suave y acabado aterciopelado.", id_prov),
                ("Gloss Brillante Voluminizador", 4.00, 10, "Labios", "Aporta brillo extremo y efecto óptico de volumen sin dejar sensación pegajosa.", id_prov),
                ("Bálsamo Hidratante Karité", 3.50, 15, "Labios", "Repara la piel reseca manteniendo los labios suaves e hidratados todo el día.", id_prov),
                ("Delineador de Labios Precisión", 4.00, 8, "Labios", "Define el contorno labial con firmeza impidiendo que el labial se desplace.", id_prov),
                ("Tinta de Labios y Mejillas", 5.50, 6, "Labios", "Otorga un rubor natural y duradero de acabado fresco sin necesidad de retoques.", id_prov),
                ("Aceite Nutritivo de Labios", 4.50, 0, "Labios", "Tratamiento con aceites naturales que ilumina y previene la resequedad labial.", id_prov),
                ("Rímel Máximo Volumen Waterproof", 6.00, 14, "Ojos y Cejas", "Alarga y da volumen extremo a las pestañas con fórmula resistente al agua.", id_prov),
                ("Paleta de Sombras Nude Pro", 10.00, 5, "Ojos y Cejas", "Incluye 12 tonos mate y satinados de alta pigmentación para cualquier estilo.", id_prov),
                ("Delineador en Gel Negro Intenso", 4.50, 9, "Ojos y Cejas", "Permite un trazo preciso y de secado rápido con acabado profesional.", id_prov),
                ("Pestañas Postizas Efecto Natural", 5.00, 0, "Ojos y Cejas", "Añaden densidad y longitud con una banda flexible y de uso reutilizable.", id_prov),
                ("Lápiz Retráctil para Cejas", 3.50, 11, "Ojos y Cejas", "Dibuja trazos ultra finos para rellenar y definir la ceja de forma natural.", id_prov),
                ("Gel Fijador Transparente de Cejas", 4.00, 7, "Ojos y Cejas", "Ordena y fija los vellos de la ceja durante todo el día sin dejar residuos blancos.", id_prov),
                ("Base Líquida Cobertura Total", 9.00, 0, "Rostro", "Empareja el tono de la piel cubriendo imperfecciones con un acabado natural.", id_prov),
                ("Corrector de Ojeras e Imperfecciones", 5.50, 13, "Rostro", "Cubre ojeras marcadas y pequeñas rojeces aportando luz a la mirada.", id_prov),
                ("Rubor en Crema Tono Durazno", 6.00, 10, "Rostro", "Aporta un color saludable y radiante a las mejillas con fácil difuminado.", id_prov),
                ("Polvo Compacto Matificante", 7.00, 8, "Rostro", "Sella la base de maquillaje controlando el brillo excesivo de la zona T.", id_prov),
                ("Iluminador en Polvo Dorado", 6.50, 4, "Rostro", "Resalta los pómulos y zonas clave del rostro con destellos de luz radiante.", id_prov),
                ("Primer Facial Suavizante de Poros", 8.00, 6, "Rostro", "Acondiciona la piel, atenúa la textura de los poros y prolonga la base.", id_prov),
                ("Fijador de Maquillaje Spray 24H", 6.50, 9, "Rostro", "Mantiene el maquillaje intacto, fresco y libre de pliegues por horas.", id_prov),
                ("BB Cream Hidratante SPF 30", 9.50, 0, "Rostro", "Combina hidratación facial, cobertura ligera y protección contra rayos solares.", id_prov),
                ("Kit de Brochas Profesionales (10 pzas)", 14.00, 3, "Accesorios", "Set completo para aplicar y difuminar bases, polvos y sombras fácilmente.", id_prov),
                ("Esponja Blender de Maquillaje", 2.50, 20, "Accesorios", "Permite extender productos líquidos y en crema logrando un acabado sin marcas.", id_prov),
                ("Organizador Acrílico de Cosméticos", 11.00, 5, "Accesorios", "Mantiene labiales, brochas y paletas ordenados y protegidos del polvo.", id_prov),
                ("Neceser Viajero Rosa BHM", 9.50, 7, "Accesorios", "Bolso espacioso y resistente para transportar todos tus cosméticos con seguridad.", id_prov),
                ("Rizador de Pestañas Ergonómico", 3.00, 15, "Accesorios", "Curva las pestañas desde la raíz con suavidad sin pellizcar la piel del párpado.", id_prov)
            ]
            cursor.executemany('''
                INSERT INTO productos (nombre, precio, stock, categoria, descripcion, id_proveedor)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', productos_iniciales)
            conn.commit()

        cursor.execute('SELECT COUNT(*) AS total FROM clientes')
        res_cli = cursor.fetchone()
        if res_cli and res_cli['total'] == 0:
            clientes_iniciales = [
                ("María López", "maria@email.com", "0991234567", "Activo"),
                ("Ana Torres", "ana@email.com", "0997654321", "Activo"),
                ("Sofia Benítez", "sofia@email.com", "0994455667", "Activo"),
                ("Camila Andrade", "camila@email.com", "0978899001", "Inactivo"),
                ("Valeria Mendoza", "valeria@email.com", "0962233445", "Activo")
            ]
            cursor.executemany('''
                INSERT INTO clientes (nombre, email, telefono, estado)
                VALUES (%s, %s, %s, %s)
            ''', clientes_iniciales)
            conn.commit()

        cursor.execute('SELECT COUNT(*) AS total FROM facturas')
        res_fac = cursor.fetchone()
        if res_fac and res_fac['total'] == 0:
            cursor.execute('SELECT id_cliente FROM clientes ORDER BY id_cliente LIMIT 5')
            cli_ids = cursor.fetchall()
            if cli_ids:
                facturas_iniciales = [
                    ("FAC-001", cli_ids[0]['id_cliente'], "2026-09-16", 12.50, "Pagado"),
                    ("FAC-002", cli_ids[1]['id_cliente'] if len(cli_ids) > 1 else cli_ids[0]['id_cliente'], "2026-09-17", 25.00, "Pagado"),
                    ("FAC-003", cli_ids[2]['id_cliente'] if len(cli_ids) > 2 else cli_ids[0]['id_cliente'], "2026-09-18", 18.00, "Pendiente"),
                    ("FAC-004", cli_ids[3]['id_cliente'] if len(cli_ids) > 3 else cli_ids[0]['id_cliente'], "2026-09-19", 30.50, "Pagado"),
                    ("FAC-005", cli_ids[4]['id_cliente'] if len(cli_ids) > 4 else cli_ids[0]['id_cliente'], "2026-09-20", 15.00, "Pendiente")
                ]
                cursor.executemany('''
                    INSERT INTO facturas (numero, id_cliente, fecha, total, estado)
                    VALUES (%s, %s, %s, %s, %s)
                ''', facturas_iniciales)
                conn.commit()

        # --- DETALLE DE LAS FACTURAS DE EJEMPLO ---
        cursor.execute('SELECT COUNT(*) AS total FROM detalle_factura')
        res_det = cursor.fetchone()
        if res_det and res_det['total'] == 0:
            # (número de factura, [(nombre del producto, cantidad), ...])
            detalles_iniciales = [
                ("FAC-001", [("Labial Matte Cream", 1), ("Rímel Máximo Volumen Waterproof", 1)]),                       # 12.50
                ("FAC-002", [("Kit de Brochas Profesionales (10 pzas)", 1), ("Organizador Acrílico de Cosméticos", 1)]),  # 25.00
                ("FAC-003", [("Primer Facial Suavizante de Poros", 1), ("Paleta de Sombras Nude Pro", 1)]),              # 18.00
                ("FAC-004", [("Kit de Brochas Profesionales (10 pzas)", 1), ("Organizador Acrílico de Cosméticos", 1),
                             ("Esponja Blender de Maquillaje", 1), ("Rizador de Pestañas Ergonómico", 1)]),             # 30.50
                ("FAC-005", [("Labial Matte Cream", 1), ("Delineador en Gel Negro Intenso", 1),
                             ("Gel Fijador Transparente de Cejas", 1)])                                                  # 15.00
            ]
            for numero, items in detalles_iniciales:
                cursor.execute('SELECT id_factura FROM facturas WHERE numero = %s LIMIT 1', (numero,))
                fac = cursor.fetchone()
                if not fac:
                    continue
                for nombre_prod, cant in items:
                    cursor.execute('SELECT id_producto, precio FROM productos WHERE nombre = %s LIMIT 1',
                                   (nombre_prod,))
                    prod = cursor.fetchone()
                    if not prod:
                        continue
                    subtotal = float(prod['precio']) * cant
                    cursor.execute('''
                        INSERT INTO detalle_factura
                        (id_factura, id_producto, cantidad, precio_unitario, subtotal)
                        VALUES (%s, %s, %s, %s, %s)
                    ''', (fac['id_factura'], prod['id_producto'], cant, prod['precio'], subtotal))
            conn.commit()

        cursor.close()
    except Exception as e:
        print(f">>> ERROR AL INICIALIZAR BASE DE DATOS: {e}")
        if conn is not None and conn.closed == 0:
            conn.rollback()
    finally:
        if conn is not None and conn.closed == 0:
            conn.close()


# --- RUTAS DE AUTENTICACIÓN ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        conn = obtener_conexion()
        if conn is None:
            flash('No se pudo conectar a la base de datos.', 'danger')
            return render_template('login.html', form=form)

        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE usuario = %s', (form.usuario.data,))
        usr = cursor.fetchone()
        cursor.close()
        conn.close()

        if usr and check_password_hash(usr['password'], form.password.data):
            user_obj = Usuario(usr['id_usuario'], usr['usuario'], usr['email'])
            login_user(user_obj)
            flash(f'¡Bienvenido/a, {usr["usuario"]}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')

    return render_template('login.html', form=form)


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = RegistroForm()
    if form.validate_on_submit():
        conn = obtener_conexion()
        if conn is None:
            flash('No se pudo conectar a la base de datos.', 'danger')
            return render_template('registro.html', form=form)

        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT id_usuario FROM usuarios WHERE usuario = %s OR email = %s',
                       (form.usuario.data, form.email.data))
        existente = cursor.fetchone()

        if existente:
            flash('El nombre de usuario o correo ya está registrado.', 'warning')
            cursor.close()
            conn.close()
        else:
            pass_hash = generate_password_hash(form.password.data)
            cursor.execute('''
                INSERT INTO usuarios (usuario, email, password)
                VALUES (%s, %s, %s)
            ''', (form.usuario.data, form.email.data, pass_hash))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Cuenta creada con éxito. ¡Ya puedes iniciar sesión!', 'success')
            return redirect(url_for('login'))

    return render_template('registro.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('inicio'))


@app.route('/dashboard')
@login_required
def dashboard():
    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute('SELECT COUNT(*) AS total FROM productos')
    tot_prod = cursor.fetchone()['total']

    cursor.execute('SELECT COUNT(*) AS total FROM clientes')
    tot_cli = cursor.fetchone()['total']

    cursor.execute('SELECT COUNT(*) AS total FROM proveedores')
    tot_prov = cursor.fetchone()['total']

    cursor.execute('SELECT COUNT(*) AS total FROM facturas')
    tot_fac = cursor.fetchone()['total']

    cursor.close()
    conn.close()

    metrics = {
        'total_productos': tot_prod,
        'total_clientes': tot_cli,
        'total_proveedores': tot_prov,
        'total_facturas': tot_fac
    }
    return render_template('dashboard.html', metrics=metrics)


# --- RUTAS DE LA APLICACIÓN ---

@app.route('/')
def inicio():
    return render_template('index.html', titulo="Bienvenidos a Brilla Hermosa Mujer")
    

# --- MÓDULO PRODUCTOS ---

@app.route('/productos')
@login_required
def productos():
    cat_seleccionada = request.args.get('categoria', 'Todos')
    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    query = '''
        SELECT p.*, pr.empresa AS proveedor_nombre
        FROM productos p
        LEFT JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
    '''

    if cat_seleccionada != 'Todos':
        query += ' WHERE p.categoria = %s ORDER BY p.id_producto'
        cursor.execute(query, (cat_seleccionada,))
    else:
        query += ' ORDER BY p.id_producto'
        cursor.execute(query)

    productos_db = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('productos.html', productos=productos_db, cat_seleccionada=cat_seleccionada)


@app.route('/productos/nuevo', methods=['GET', 'POST'])
@login_required
def formulario_producto():
    form = ProductoForm()

    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT id_proveedor, empresa FROM proveedores ORDER BY id_proveedor')
    proveedores_db = cursor.fetchall()
    form.id_proveedor.choices = [(p['id_proveedor'], p['empresa']) for p in proveedores_db]

    if form.validate_on_submit():
        cursor_insert = conn.cursor()
        cursor_insert.execute('''
            INSERT INTO productos (nombre, precio, stock, categoria, descripcion, id_proveedor)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (
            form.nombre.data,
            form.precio.data,
            form.stock.data,
            form.categoria.data,
            form.descripcion.data,
            form.id_proveedor.data
        ))
        conn.commit()
        cursor_insert.close()
        cursor.close()
        conn.close()

        flash('Producto guardado correctamente.', 'success')
        return redirect(url_for('productos'))

    cursor.close()
    conn.close()
    return render_template('formulario_producto.html', form=form)


@app.route('/productos/editar/<int:id_producto>', methods=['GET', 'POST'])
@login_required
def editar_producto(id_producto):
    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute('SELECT * FROM productos WHERE id_producto = %s', (id_producto,))
    producto = cursor.fetchone()

    if not producto:
        cursor.close()
        conn.close()
        flash('El producto solicitado no existe.', 'danger')
        return redirect(url_for('productos'))

    form = ProductoForm(data=producto)

    cursor.execute('SELECT id_proveedor, empresa FROM proveedores ORDER BY id_proveedor')
    proveedores_db = cursor.fetchall()
    form.id_proveedor.choices = [(p['id_proveedor'], p['empresa']) for p in proveedores_db]

    if request.method == 'GET':
        form.id_proveedor.data = producto.get('id_proveedor')

    if form.validate_on_submit():
        cursor_update = conn.cursor()
        cursor_update.execute('''
            UPDATE productos
            SET nombre = %s, precio = %s, stock = %s, categoria = %s, descripcion = %s, id_proveedor = %s
            WHERE id_producto = %s
        ''', (
            form.nombre.data,
            form.precio.data,
            form.stock.data,
            form.categoria.data,
            form.descripcion.data,
            form.id_proveedor.data,
            id_producto
        ))
        conn.commit()
        cursor_update.close()
        cursor.close()
        conn.close()

        flash('Producto actualizado correctamente.', 'success')
        return redirect(url_for('productos'))

    cursor.close()
    conn.close()
    return render_template('formulario_producto.html', form=form, producto=producto)


@app.route('/productos/eliminar/<int:id_producto>', methods=['POST'])
@login_required
def eliminar_producto(id_producto):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productos WHERE id_producto = %s', (id_producto,))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Producto eliminado correctamente.', 'warning')
    return redirect(url_for('productos'))


# --- MÓDULO CLIENTES ---

@app.route('/clientes')
@login_required
def clientes():
    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT id_cliente AS id, nombre, email, telefono, estado FROM clientes ORDER BY id_cliente')
    clientes_db = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('clientes.html', clientes=clientes_db)


@app.route('/clientes/nuevo', methods=['GET', 'POST'])
@login_required
def formulario_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clientes (nombre, email, telefono, estado)
            VALUES (%s, %s, %s, %s)
        ''', (form.nombre.data, form.email.data, form.telefono.data, form.estado.data))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Cliente guardado correctamente.', 'success')
        return redirect(url_for('clientes'))
    return render_template('formulario_cliente.html', form=form)


@app.route('/clientes/editar/<int:cliente_id>', methods=['GET', 'POST'])
@login_required
def editar_cliente(cliente_id):
    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM clientes WHERE id_cliente = %s', (cliente_id,))
    cliente = cursor.fetchone()

    if not cliente:
        cursor.close()
        conn.close()
        flash('El cliente solicitado no existe.', 'danger')
        return redirect(url_for('clientes'))

    form = ClienteForm(data=cliente)
    if form.validate_on_submit():
        cursor_update = conn.cursor()
        cursor_update.execute('''
            UPDATE clientes
            SET nombre = %s, email = %s, telefono = %s, estado = %s
            WHERE id_cliente = %s
        ''', (form.nombre.data, form.email.data, form.telefono.data, form.estado.data, cliente_id))
        conn.commit()
        cursor_update.close()
        cursor.close()
        conn.close()
        flash('Cliente actualizado correctamente.', 'success')
        return redirect(url_for('clientes'))

    cursor.close()
    conn.close()
    return render_template('formulario_cliente.html', form=form, cliente=cliente)


@app.route('/clientes/eliminar/<int:cliente_id>', methods=['POST'])
@login_required
def eliminar_cliente(cliente_id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE id_cliente = %s', (cliente_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Cliente eliminado correctamente.', 'warning')
    return redirect(url_for('clientes'))


# --- MÓDULO PROVEEDORES ---

@app.route('/proveedores')
@login_required
def proveedores():
    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT id_proveedor AS id, empresa, contacto, telefono, ciudad FROM proveedores ORDER BY id_proveedor')
    proveedores_db = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('proveedores.html', proveedores=proveedores_db)


@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
@login_required
def formulario_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO proveedores (empresa, contacto, telefono, ciudad)
            VALUES (%s, %s, %s, %s)
        ''', (form.empresa.data, form.contacto.data, form.telefono.data, form.ciudad.data))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Proveedor guardado correctamente.', 'success')
        return redirect(url_for('proveedores'))
    return render_template('formulario_proveedor.html', form=form)


@app.route('/proveedores/editar/<int:proveedor_id>', methods=['GET', 'POST'])
@login_required
def editar_proveedor(proveedor_id):
    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM proveedores WHERE id_proveedor = %s', (proveedor_id,))
    proveedor = cursor.fetchone()

    if not proveedor:
        cursor.close()
        conn.close()
        flash('El proveedor solicitado no existe.', 'danger')
        return redirect(url_for('proveedores'))

    form = ProveedorForm(data=proveedor)
    if form.validate_on_submit():
        cursor_update = conn.cursor()
        cursor_update.execute('''
            UPDATE proveedores
            SET empresa = %s, contacto = %s, telefono = %s, ciudad = %s
            WHERE id_proveedor = %s
        ''', (form.empresa.data, form.contacto.data, form.telefono.data, form.ciudad.data, proveedor_id))
        conn.commit()
        cursor_update.close()
        cursor.close()
        conn.close()
        flash('Proveedor actualizado correctamente.', 'success')
        return redirect(url_for('proveedores'))

    cursor.close()
    conn.close()
    return render_template('formulario_proveedor.html', form=form, proveedor=proveedor)


@app.route('/proveedores/eliminar/<int:proveedor_id>', methods=['POST'])
@login_required
def eliminar_proveedor(proveedor_id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM proveedores WHERE id_proveedor = %s', (proveedor_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Proveedor eliminado correctamente.', 'warning')
    return redirect(url_for('proveedores'))


# --- MÓDULO FACTURACIÓN ---

@app.route('/facturacion')
@login_required
def facturacion():
    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('''
        SELECT f.numero, c.nombre AS cliente, TO_CHAR(f.fecha, 'YYYY-MM-DD') AS fecha,
               f.total, f.estado,
               COALESCE(STRING_AGG(p.nombre || ' (x' || d.cantidad || ')', ', '), 'Sin productos') AS productos
        FROM facturas f
        LEFT JOIN clientes c ON f.id_cliente = c.id_cliente
        LEFT JOIN detalle_factura d ON d.id_factura = f.id_factura
        LEFT JOIN productos p ON d.id_producto = p.id_producto
        GROUP BY f.id_factura, f.numero, c.nombre, f.fecha, f.total, f.estado
        ORDER BY f.id_factura
    ''')
    facturas_db = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('facturacion.html', facturas=facturas_db)


@app.route('/facturacion/nuevo', methods=['GET', 'POST'])
@login_required
def formulario_facturacion():
    form = FacturacionForm()

    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT id_producto, nombre, categoria, precio, stock FROM productos ORDER BY nombre')
    productos_db = cursor.fetchall()

    if form.validate_on_submit():
        ids = request.form.getlist('id_producto[]')
        cantidades = request.form.getlist('cantidad[]')

        items = []
        for i, c in zip(ids, cantidades):
            if i and c and int(c) > 0:
                items.append((int(i), int(c)))

        if not items:
            flash('Debes agregar al menos un producto.', 'danger')
        else:
            try:
                total = 0
                detalles = []
                error = None

                for id_prod, cant in items:
                    # FOR UPDATE bloquea la fila para evitar vender stock dos veces
                    cursor.execute(
                        'SELECT nombre, precio, stock FROM productos WHERE id_producto = %s FOR UPDATE',
                        (id_prod,))
                    p = cursor.fetchone()
                    if not p:
                        error = 'Un producto seleccionado no existe.'
                        break
                    if cant > p['stock']:
                        error = (f'Stock insuficiente de "{p["nombre"]}": '
                                 f'pediste {cant} y solo quedan {p["stock"]}.')
                        break
                    subtotal = float(p['precio']) * cant
                    total += subtotal
                    detalles.append((id_prod, cant, p['precio'], subtotal))

                if error:
                    conn.rollback()
                    flash(error, 'danger')
                else:
                    # Cliente
                    cursor.execute('SELECT id_cliente FROM clientes WHERE nombre = %s LIMIT 1',
                                   (form.cliente.data,))
                    cli = cursor.fetchone()
                    if not cli:
                        cursor.execute('''
                            INSERT INTO clientes (nombre, email, telefono, estado)
                            VALUES (%s, %s, %s, %s) RETURNING id_cliente
                        ''', (form.cliente.data, 'sin_email@dominio.com', '0000000000', 'Activo'))
                        id_cliente = cursor.fetchone()['id_cliente']
                    else:
                        id_cliente = cli['id_cliente']

                    # Factura
                    cursor.execute('''
                        INSERT INTO facturas (numero, id_cliente, fecha, total, estado)
                        VALUES (%s, %s, %s, %s, %s) RETURNING id_factura
                    ''', (form.numero.data, id_cliente, form.fecha.data, total, form.estado.data))
                    id_factura = cursor.fetchone()['id_factura']

                    # Detalle + descontar stock
                    for id_prod, cant, precio, subtotal in detalles:
                        cursor.execute('''
                            INSERT INTO detalle_factura
                            (id_factura, id_producto, cantidad, precio_unitario, subtotal)
                            VALUES (%s, %s, %s, %s, %s)
                        ''', (id_factura, id_prod, cant, precio, subtotal))
                        cursor.execute('UPDATE productos SET stock = stock - %s WHERE id_producto = %s',
                                       (cant, id_prod))

                    conn.commit()
                    cursor.close()
                    conn.close()
                    flash('Factura guardada correctamente.', 'success')
                    return redirect(url_for('detalle_factura', numero=form.numero.data))
            except Exception as e:
                conn.rollback()
                flash(f'Error al guardar la factura: {e}', 'danger')

    cursor.close()
    conn.close()
    return render_template('formulario_facturacion.html', form=form, productos=productos_db)


@app.route('/facturacion/detalle/<string:numero>')
@login_required
def detalle_factura(numero):
    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute('''
        SELECT f.id_factura, f.numero, c.nombre AS cliente,
               TO_CHAR(f.fecha, 'YYYY-MM-DD') AS fecha, f.total, f.estado
        FROM facturas f
        LEFT JOIN clientes c ON f.id_cliente = c.id_cliente
        WHERE f.numero = %s LIMIT 1
    ''', (numero,))
    factura = cursor.fetchone()

    if not factura:
        cursor.close()
        conn.close()
        flash('La factura solicitada no existe.', 'danger')
        return redirect(url_for('facturacion'))

    cursor.execute('''
        SELECT p.nombre AS producto, p.categoria, d.precio_unitario,
               d.cantidad, d.subtotal, p.stock AS stock_restante
        FROM detalle_factura d
        JOIN productos p ON d.id_producto = p.id_producto
        WHERE d.id_factura = %s
    ''', (factura['id_factura'],))
    detalles = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('detalle_factura.html', factura=factura, detalles=detalles)


@app.route('/facturacion/editar/<string:numero>', methods=['GET', 'POST'])
@login_required
def editar_factura(numero):
    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('''
        SELECT f.numero, c.nombre AS cliente, TO_CHAR(f.fecha, 'YYYY-MM-DD') AS fecha, f.total, f.estado
        FROM facturas f
        LEFT JOIN clientes c ON f.id_cliente = c.id_cliente
        WHERE f.numero = %s
        LIMIT 1
    ''', (numero,))
    factura = cursor.fetchone()

    if not factura:
        cursor.close()
        conn.close()
        flash('La factura solicitada no existe.', 'danger')
        return redirect(url_for('facturacion'))

    form = FacturacionForm(data={
        'numero': factura['numero'],
        'cliente': factura['cliente'],
        'fecha': factura['fecha'],
        'total': float(factura['total']),
        'estado': factura['estado']
    })

    if form.validate_on_submit():
        cursor.execute('SELECT id_cliente FROM clientes WHERE nombre = %s LIMIT 1', (form.cliente.data,))
        cli = cursor.fetchone()

        if not cli:
            cursor.execute('''
                INSERT INTO clientes (nombre, email, telefono, estado)
                VALUES (%s, %s, %s, %s)
                RETURNING id_cliente
            ''', (form.cliente.data, 'sin_email@dominio.com', '0000000000', 'Activo'))
            id_cliente = cursor.fetchone()['id_cliente']
        else:
            id_cliente = cli['id_cliente']

        cursor.execute('''
            UPDATE facturas
            SET numero = %s, id_cliente = %s, fecha = %s, total = %s, estado = %s
            WHERE numero = %s
        ''', (form.numero.data, id_cliente, form.fecha.data, form.total.data, form.estado.data, numero))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Factura actualizada correctamente.', 'success')
        return redirect(url_for('facturacion'))

    cursor.close()
    conn.close()
    return render_template('formulario_facturacion.html', form=form, factura=factura)


@app.route('/facturacion/eliminar/<string:numero>', methods=['POST'])
@login_required
def eliminar_factura(numero):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM facturas WHERE numero = %s', (numero,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Factura eliminada correctamente.', 'warning')
    return redirect(url_for('facturacion'))


if __name__ == '__main__':
    print(">>> Conectando e inicializando la base de datos PostgreSQL...")
    inicializar_base_datos()
    print(">>> Iniciando servidor Flask...")
    app.run(debug=True)