import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_semana_12_desarrollo_web'

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'ferreteria.db')

def obtener_conexion_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def inicializar_base_datos():
    conn = obtener_conexion_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL,
            categoria TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            imagen TEXT DEFAULT 'img/Maquillaje.png'
        )
    ''')
    
    cursor.execute('SELECT COUNT(*) FROM productos')
    if cursor.fetchone()[0] == 0:
        productos_iniciales = [
            ("Labial Matte Cream", 6.50, 12, "Labios", "Brinda color intenso de larga duración con textura suave y acabado aterciopelado.", "img/Maquillaje.png"),
            ("Gloss Brillante Voluminizador", 4.00, 10, "Labios", "Aporta brillo extremo y efecto óptico de volumen sin dejar sensación pegajosa.", "img/Maquillaje.png"),
            ("Bálsamo Hidratante Karité", 3.50, 15, "Labios", "Repara la piel reseca manteniendo los labios suaves e hidratados todo el día.", "img/Maquillaje.png"),
            ("Delineador de Labios Precisión", 4.00, 8, "Labios", "Define el contorno labial con firmeza impidiendo que el labial se desplace.", "img/Maquillaje.png"),
            ("Tinta de Labios y Mejillas", 5.50, 6, "Labios", "Otorga un rubor natural y duradero de acabado fresco sin necesidad de retoques.", "img/Maquillaje.png"),
            ("Aceite Nutritivo de Labios", 4.50, 0, "Labios", "Tratamiento con aceites naturales que ilumina y previene la resequedad labial.", "img/Maquillaje.png"),
            ("Rímel Máximo Volumen Waterproof", 6.00, 14, "Ojos y Cejas", "Alarga y da volumen extremo a las pestañas con fórmula resistente al agua.", "img/Maquillaje.png"),
            ("Paleta de Sombras Nude Pro", 10.00, 5, "Ojos y Cejas", "Incluye 12 tonos mate y satinados de alta pigmentación para cualquier estilo.", "img/Maquillaje.png"),
            ("Delineador en Gel Negro Intenso", 4.50, 9, "Ojos y Cejas", "Permite un trazo preciso y de secado rápido con acabado profesional.", "img/Maquillaje.png"),
            ("Pestañas Postizas Efecto Natural", 5.00, 0, "Ojos y Cejas", "Añaden densidad y longitud con una banda flexible y de uso reutilizable.", "img/Maquillaje.png"),
            ("Lápiz Retráctil para Cejas", 3.50, 11, "Ojos y Cejas", "Dibuja trazos ultra finos para rellenar y definir la ceja de forma natural.", "img/Maquillaje.png"),
            ("Gel Fijador Transparente de Cejas", 4.00, 7, "Ojos y Cejas", "Ordena y fija los vellos de la ceja durante todo el día sin dejar residuos blancos.", "img/Maquillaje.png"),
            ("Base Líquida Cobertura Total", 9.00, 0, "Rostro", "Empareja el tono de la piel cubriendo imperfecciones con un acabado natural.", "img/Maquillaje.png"),
            ("Corrector de Ojeras e Imperfecciones", 5.50, 13, "Rostro", "Cubre ojeras marcadas y pequeñas rojeces aportando luz a la mirada.", "img/Maquillaje.png"),
            ("Rubor en Crema Tono Durazno", 6.00, 10, "Rostro", "Aporta un color saludable y radiante a las mejillas con fácil difuminado.", "img/Maquillaje.png"),
            ("Polvo Compacto Matificante", 7.00, 8, "Rostro", "Sella la base de maquillaje controlando el brillo excesivo de la zona T.", "img/Maquillaje.png"),
            ("Iluminador en Polvo Dorado", 6.50, 4, "Rostro", "Resalta los pómulos y zonas clave del rostro con destellos de luz radiante.", "img/Maquillaje.png"),
            ("Primer Facial Suavizante de Poros", 8.00, 6, "Rostro", "Acondiciona la piel, atenúa la textura de los poros y prolonga la base.", "img/Maquillaje.png"),
            ("Fijador de Maquillaje Spray 24H", 6.50, 9, "Rostro", "Mantiene el maquillaje intacto, fresco y libre de pliegues por horas.", "img/Maquillaje.png"),
            ("BB Cream Hidratante SPF 30", 9.50, 0, "Rostro", "Combina hidratación facial, cobertura ligera y protección contra rayos solares.", "img/Maquillaje.png"),
            ("Kit de Brochas Profesionales (10 pzas)", 14.00, 3, "Accesorios", "Set completo para aplicar y difuminar bases, polvos y sombras fácilmente.", "img/Maquillaje.png"),
            ("Esponja Blender de Maquillaje", 2.50, 20, "Accesorios", "Permite extender productos líquidos y en crema logrando un acabado sin marcas.", "img/Maquillaje.png"),
            ("Organizador Acrílico de Cosméticos", 11.00, 5, "Accesorios", "Mantiene labiales, brochas y paletas ordenados y protegidos del polvo.", "img/Maquillaje.png"),
            ("Neceser Viajero Rosa BHM", 9.50, 7, "Accesorios", "Bolso espacioso y resistente para transportar todos tus cosméticos con seguridad.", "img/Maquillaje.png"),
            ("Rizador de Pestañas Ergonómico", 3.00, 15, "Accesorios", "Curva las pestañas desde la raíz con suavidad sin pellizcar la piel del párpado.", "img/Maquillaje.png")
        ]
        cursor.executemany('''
            INSERT INTO productos (nombre, precio, stock, categoria, descripcion, imagen)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', productos_iniciales)
    
    conn.commit()
    conn.close()

inicializar_base_datos()

CLIENTES = [
    {"id": 1, "nombre": "María López", "email": "maria@email.com", "telefono": "0991234567", "estado": "Activo"},
    {"id": 2, "nombre": "Ana Torres", "email": "ana@email.com", "telefono": "0997654321", "estado": "Activo"}
]

PROVEEDORES = [
    {"id": 1, "empresa": "Distribuidora Belleza S.A.", "contacto": "Carlos Ruiz", "telefono": "022345678", "ciudad": "Quito"}
]

FACTURAS = [
    {"numero": "FAC-001", "cliente": "María López", "fecha": "2026-09-16", "total": 12.50, "estado": "Pagado"}
]

@app.route('/')
def inicio():
    return render_template('index.html', titulo="Bienvenidos a Brilla Hermosa Mujer")

@app.route('/productos')
def productos():
    cat_seleccionada = request.args.get('categoria', 'Todos')
    conn = obtener_conexion_db()
    cursor = conn.cursor()
    
    if cat_seleccionada != 'Todos':
        cursor.execute('SELECT * FROM productos WHERE categoria = ?', (cat_seleccionada,))
    else:
        cursor.execute('SELECT * FROM productos')
        
    productos_db = cursor.fetchall()
    conn.close()
    
    return render_template('productos.html', productos=productos_db, cat_seleccionada=cat_seleccionada)

@app.route('/productos/nuevo', methods=['GET', 'POST'])
def formulario_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        conn = obtener_conexion_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO productos (nombre, precio, stock, categoria, descripcion, imagen)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            form.nombre.data,
            form.precio.data,
            form.stock.data,
            form.categoria.data,
            form.descripcion.data,
            "img/Maquillaje.png"
        ))
        conn.commit()
        conn.close()
        
        flash('Producto guardado correctamente.', 'success')
        return redirect(url_for('productos'))
    return render_template('formulario_producto.html', form=form)

@app.route('/productos/eliminar/<int:producto_id>', methods=['POST'])
def eliminar_producto(producto_id):
    conn = obtener_conexion_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productos WHERE id = ?', (producto_id,))
    conn.commit()
    conn.close()
    
    flash('Producto eliminado correctamente.', 'warning')
    return redirect(url_for('productos'))

@app.route('/clientes')
def clientes():
    return render_template('clientes.html', clientes=CLIENTES)

@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def formulario_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        nuevo_c = {
            "id": len(CLIENTES) + 1,
            "nombre": form.nombre.data,
            "email": form.email.data,
            "telefono": form.telefono.data,
            "estado": form.estado.data
        }
        CLIENTES.append(nuevo_c)
        flash('Cliente guardado correctamente.', 'success')
        return redirect(url_for('clientes'))
    return render_template('formulario_cliente.html', form=form)

@app.route('/clientes/eliminar/<int:cliente_id>', methods=['POST'])
def eliminar_cliente(cliente_id):
    global CLIENTES
    CLIENTES = [c for c in CLIENTES if c['id'] != cliente_id]
    flash('Cliente eliminado correctamente.', 'warning')
    return redirect(url_for('clientes'))

@app.route('/proveedores')
def proveedores():
    return render_template('proveedores.html', proveedores=PROVEEDORES)

@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
def formulario_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        nuevo_pr = {
            "id": len(PROVEEDORES) + 1,
            "empresa": form.empresa.data,
            "contacto": form.contacto.data,
            "telefono": form.telefono.data,
            "ciudad": form.ciudad.data
        }
        PROVEEDORES.append(nuevo_pr)
        flash('Proveedor guardado correctamente.', 'success')
        return redirect(url_for('proveedores'))
    return render_template('formulario_proveedor.html', form=form)

@app.route('/proveedores/eliminar/<int:proveedor_id>', methods=['POST'])
def eliminar_proveedor(proveedor_id):
    global PROVEEDORES
    PROVEEDORES = [pr for pr in PROVEEDORES if pr['id'] != proveedor_id]
    flash('Proveedor eliminado correctamente.', 'warning')
    return redirect(url_for('proveedores'))

@app.route('/facturacion')
def facturacion():
    return render_template('facturacion.html', facturas=FACTURAS)

@app.route('/facturacion/nuevo', methods=['GET', 'POST'])
def formulario_facturacion():
    form = FacturacionForm()
    if form.validate_on_submit():
        nueva_f = {
            "numero": form.numero.data,
            "cliente": form.cliente.data,
            "fecha": str(form.fecha.data),
            "total": form.total.data,
            "estado": form.estado.data
        }
        FACTURAS.append(nueva_f)
        flash('Factura guardada correctamente.', 'success')
        return redirect(url_for('facturacion'))
    return render_template('formulario_facturacion.html', form=form)

@app.route('/facturacion/eliminar/<string:numero>', methods=['POST'])
def eliminar_factura(numero):
    global FACTURAS
    FACTURAS = [f for f in FACTURAS if f['numero'] != numero]
    flash('Factura eliminada correctamente.', 'warning')
    return redirect(url_for('facturacion'))

if __name__ == '__main__':
    app.run(debug=True)