import os
from flask import Flask, render_template, request, redirect, url_for, flash
from conexion.conexion import obtener_conexion
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_semana_13_desarrollo_web'

def inicializar_base_datos():
    """Puebla datos iniciales en MySQL si las tablas están vacías."""
    conn = None
    try:
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)
        
        # 1. Proveedores iniciales
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

        # Obtener el ID del primer proveedor para asociarlo a los productos
        cursor.execute('SELECT id_proveedor FROM proveedores LIMIT 1')
        prov_default = cursor.fetchone()
        id_prov = prov_default['id_proveedor'] if prov_default else None

        # 2. Productos iniciales
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

        # 3. Clientes iniciales
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

        # 4. Facturas iniciales
        cursor.execute('SELECT COUNT(*) AS total FROM facturas')
        res_fac = cursor.fetchone()
        if res_fac and res_fac['total'] == 0:
            cursor.execute('SELECT id_cliente FROM clientes LIMIT 5')
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

        cursor.close()
    except Exception as e:
        print(f">>> ERROR AL INICIALIZAR BASE DE DATOS: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()

# --- RUTAS DE LA APLICACIÓN ---

@app.route('/')
def inicio():
    return render_template('index.html', titulo="Bienvenidos a Brilla Hermosa Mujer")

# --- MÓDULO PRODUCTOS ---

@app.route('/productos')
def productos():
    cat_seleccionada = request.args.get('categoria', 'Todos')
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    
    query = '''
        SELECT p.*, pr.empresa AS proveedor_nombre 
        FROM productos p 
        LEFT JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
    '''
    
    if cat_seleccionada != 'Todos':
        query += ' WHERE p.categoria = %s'
        cursor.execute(query, (cat_seleccionada,))
    else:
        cursor.execute(query)
        
    productos_db = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('productos.html', productos=productos_db, cat_seleccionada=cat_seleccionada)

@app.route('/productos/nuevo', methods=['GET', 'POST'])
def formulario_producto():
    form = ProductoForm()
    
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id_proveedor, empresa FROM proveedores')
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
def editar_producto(id_producto):
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('SELECT * FROM productos WHERE id_producto = %s', (id_producto,))
    producto = cursor.fetchone()
    
    if not producto:
        cursor.close()
        conn.close()
        flash('El producto solicitado no existe.', 'danger')
        return redirect(url_for('productos'))
        
    form = ProductoForm(data=producto)
    
    cursor.execute('SELECT id_proveedor, empresa FROM proveedores')
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
def clientes():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id_cliente AS id, nombre, email, telefono, estado FROM clientes')
    clientes_db = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('clientes.html', clientes=clientes_db)

@app.route('/clientes/nuevo', methods=['GET', 'POST'])
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

# NUEVA RUTA: Editar Cliente (Agregada para cumplir con la guía)
@app.route('/clientes/editar/<int:cliente_id>', methods=['GET', 'POST'])
def editar_cliente(cliente_id):
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
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
def proveedores():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id_proveedor AS id, empresa, contacto, telefono, ciudad FROM proveedores')
    proveedores_db = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('proveedores.html', proveedores=proveedores_db)

@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
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

# NUEVA RUTA: Editar Proveedor (Agregada para cumplir con la guía)
@app.route('/proveedores/editar/<int:proveedor_id>', methods=['GET', 'POST'])
def editar_proveedor(proveedor_id):
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
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
def facturacion():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT f.numero, c.nombre AS cliente, DATE_FORMAT(f.fecha, '%Y-%m-%d') AS fecha, f.total, f.estado
        FROM facturas f
        LEFT JOIN clientes c ON f.id_cliente = c.id_cliente
    ''')
    facturas_db = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('facturacion.html', facturas=facturas_db)

@app.route('/facturacion/nuevo', methods=['GET', 'POST'])
def formulario_facturacion():
    form = FacturacionForm()
    if form.validate_on_submit():
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute('SELECT id_cliente FROM clientes WHERE nombre = %s LIMIT 1', (form.cliente.data,))
        cli = cursor.fetchone()
        
        if not cli:
            cursor.execute('''
                INSERT INTO clientes (nombre, email, telefono, estado)
                VALUES (%s, %s, %s, %s)
            ''', (form.cliente.data, 'sin_email@dominio.com', '0000000000', 'Activo'))
            conn.commit()
            id_cliente = cursor.lastrowid
        else:
            id_cliente = cli['id_cliente']

        cursor.execute('''
            INSERT INTO facturas (numero, id_cliente, fecha, total, estado)
            VALUES (%s, %s, %s, %s, %s)
        ''', (form.numero.data, id_cliente, form.fecha.data, form.total.data, form.estado.data))
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Factura guardada correctamente.', 'success')
        return redirect(url_for('facturacion'))
    return render_template('formulario_facturacion.html', form=form)

@app.route('/facturacion/eliminar/<string:numero>', methods=['POST'])
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
    print(">>> Conectando e inicializando la base de datos MySQL...")
    inicializar_base_datos()
    print(">>> Iniciando servidor Flask...")
    app.run(debug=True)