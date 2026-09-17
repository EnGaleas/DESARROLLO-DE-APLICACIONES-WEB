from flask import Flask, render_template, request, redirect, url_for, flash
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_semana_11_desarrollo_web'

PRODUCTOS = [
    # --- LABIOS ---
    {"id": 1, "nombre": "Labial Matte Cream", "categoria": "Labios", "descripcion": "Brinda color intenso de larga duración con textura suave y acabado aterciopelado.", "precio": 6.50, "stock": 12, "imagen": "img/Maquillaje.png"},
    {"id": 2, "nombre": "Gloss Brillante Voluminizador", "categoria": "Labios", "descripcion": "Aporta brillo extremo y efecto óptico de volumen sin dejar sensación pegajosa.", "precio": 4.00, "stock": 10, "imagen": "img/Maquillaje.png"},
    {"id": 3, "nombre": "Bálsamo Hidratante Karité", "categoria": "Labios", "descripcion": "Repara la piel reseca manteniendo los labios suaves e hidratados todo el día.", "precio": 3.50, "stock": 15, "imagen": "img/Maquillaje.png"},
    {"id": 4, "nombre": "Delineador de Labios Precisión", "categoria": "Labios", "descripcion": "Define el contorno labial con firmeza impidiendo que el labial se desplace.", "precio": 4.00, "stock": 8, "imagen": "img/Maquillaje.png"},
    {"id": 5, "nombre": "Tinta de Labios y Mejillas", "categoria": "Labios", "descripcion": "Otorga un rubor natural y duradero de acabado fresco sin necesidad de retoques.", "precio": 5.50, "stock": 6, "imagen": "img/Maquillaje.png"},
    {"id": 6, "nombre": "Aceite Nutritivo de Labios", "categoria": "Labios", "descripcion": "Tratamiento con aceites naturales que ilumina y previene la resequedad labial.", "precio": 4.50, "stock": 0, "imagen": "img/Maquillaje.png"},

    # --- OJOS Y CEJAS ---
    {"id": 7, "nombre": "Rímel Máximo Volumen Waterproof", "categoria": "Ojos y Cejas", "descripcion": "Alarga y da volumen extremo a las pestañas con fórmula resistente al agua.", "precio": 6.00, "stock": 14, "imagen": "img/Maquillaje.png"},
    {"id": 8, "nombre": "Paleta de Sombras Nude Pro", "categoria": "Ojos y Cejas", "descripcion": "Incluye 12 tonos mate y satinados de alta pigmentación para cualquier estilo.", "precio": 10.00, "stock": 5, "imagen": "img/Maquillaje.png"},
    {"id": 9, "nombre": "Delineador en Gel Negro Intenso", "categoria": "Ojos y Cejas", "descripcion": "Permite un trazo preciso y de secado rápido con acabado profesional.", "precio": 4.50, "stock": 9, "imagen": "img/Maquillaje.png"},
    {"id": 10, "nombre": "Pestañas Postizas Efecto Natural", "categoria": "Ojos y Cejas", "descripcion": "Añaden densidad y longitud con una banda flexible y de uso reutilizable.", "precio": 5.00, "stock": 0, "imagen": "img/Maquillaje.png"},
    {"id": 11, "nombre": "Lápiz Retráctil para Cejas", "categoria": "Ojos y Cejas", "descripcion": "Dibuja trazos ultra finos para rellenar y definir la ceja de forma natural.", "precio": 3.50, "stock": 11, "imagen": "img/Maquillaje.png"},
    {"id": 12, "nombre": "Gel Fijador Transparente de Cejas", "categoria": "Ojos y Cejas", "descripcion": "Ordena y fija los vellos de la ceja durante todo el día sin dejar residuos blancos.", "precio": 4.00, "stock": 7, "imagen": "img/Maquillaje.png"},

    # --- ROSTRO ---
    {"id": 13, "nombre": "Base Líquida Cobertura Total", "categoria": "Rostro", "descripcion": "Empareja el tono de la piel cubriendo imperfecciones con un acabado natural.", "precio": 9.00, "stock": 0, "imagen": "img/Maquillaje.png"},
    {"id": 14, "nombre": "Corrector de Ojeras e Imperfecciones", "categoria": "Rostro", "descripcion": "Cubre ojeras marcadas y pequeñas rojeces aportando luz a la mirada.", "precio": 5.50, "stock": 13, "imagen": "img/Maquillaje.png"},
    {"id": 15, "nombre": "Rubor en Crema Tono Durazno", "categoria": "Rostro", "descripcion": "Aporta un color saludable y radiante a las mejillas con fácil difuminado.", "precio": 6.00, "stock": 10, "imagen": "img/Maquillaje.png"},
    {"id": 16, "nombre": "Polvo Compacto Matificante", "categoria": "Rostro", "descripcion": "Sella la base de maquillaje controlando el brillo excesivo de la zona T.", "precio": 7.00, "stock": 8, "imagen": "img/Maquillaje.png"},
    {"id": 17, "nombre": "Iluminador en Polvo Dorado", "categoria": "Rostro", "descripcion": "Resalta los pómulos y zonas clave del rostro con destellos de luz radiante.", "precio": 6.50, "stock": 4, "imagen": "img/Maquillaje.png"},
    {"id": 18, "nombre": "Primer Facial Suavizante de Poros", "categoria": "Rostro", "descripcion": "Acondiciona la piel, atenúa la textura de los poros y prolonga la base.", "precio": 8.00, "stock": 6, "imagen": "img/Maquillaje.png"},
    {"id": 19, "nombre": "Fijador de Maquillaje Spray 24H", "categoria": "Rostro", "descripcion": "Mantiene el maquillaje intacto, fresco y libre de pliegues por horas.", "precio": 6.50, "stock": 9, "imagen": "img/Maquillaje.png"},
    {"id": 20, "nombre": "BB Cream Hidratante SPF 30", "categoria": "Rostro", "descripcion": "Combina hidratación facial, cobertura ligera y protección contra rayos solares.", "precio": 9.50, "stock": 0, "imagen": "img/Maquillaje.png"},

    # --- ACCESORIOS ---
    {"id": 21, "nombre": "Kit de Brochas Profesionales (10 pzas)", "categoria": "Accesorios", "descripcion": "Set completo para aplicar y difuminar bases, polvos y sombras fácilmente.", "precio": 14.00, "stock": 3, "imagen": "img/Maquillaje.png"},
    {"id": 22, "nombre": "Esponja Blender de Maquillaje", "categoria": "Accesorios", "descripcion": "Permite extender productos líquidos y en crema logrando un acabado sin marcas.", "precio": 2.50, "stock": 20, "imagen": "img/Maquillaje.png"},
    {"id": 23, "nombre": "Organizador Acrílico de Cosméticos", "categoria": "Accesorios", "descripcion": "Mantiene labiales, brochas y paletas ordenados y protegidos del polvo.", "precio": 11.00, "stock": 5, "imagen": "img/Maquillaje.png"},
    {"id": 24, "nombre": "Neceser Viajero Rosa BHM", "categoria": "Accesorios", "descripcion": "Bolso espacioso y resistente para transportar todos tus cosméticos con seguridad.", "precio": 9.50, "stock": 7, "imagen": "img/Maquillaje.png"},
    {"id": 25, "nombre": "Rizador de Pestañas Ergonómico", "categoria": "Accesorios", "descripcion": "Curva las pestañas desde la raíz con suavidad sin pellizcar la piel del párpado.", "precio": 3.00, "stock": 15, "imagen": "img/Maquillaje.png"}
]

CLIENTES = [
    {"id": 1, "nombre": "María López", "email": "maria@email.com", "telefono": "0991234567", "estado": "Activo"},
    {"id": 2, "nombre": "Ana Torres", "email": "ana@email.com", "telefono": "0997654321", "estado": "Activo"},
    {"id": 3, "nombre": "Carla Mendoza", "email": "carla@email.com", "telefono": "0981122334", "estado": "Inactivo"},
    {"id": 4, "nombre": "Diana Gómez", "email": "diana@email.com", "telefono": "0975566778", "estado": "Activo"}
]

PROVEEDORES = [
    {"id": 1, "empresa": "Distribuidora Belleza S.A.", "contacto": "Carlos Ruiz", "telefono": "022345678", "ciudad": "Quito"},
    {"id": 2, "empresa": "Cosméticos del Ecuador", "contacto": "Laura Paez", "telefono": "042889900", "ciudad": "Guayaquil"},
    {"id": 3, "empresa": "Importadora Glamour", "contacto": "Sofía Viteri", "telefono": "072112233", "ciudad": "Cuenca"}
]

FACTURAS = [
    {"numero": "FAC-001", "cliente": "María López", "fecha": "2026-09-16", "total": 12.50, "estado": "Pagado"},
    {"numero": "FAC-002", "cliente": "Ana Torres", "fecha": "2026-09-16", "total": 24.00, "estado": "Pagado"},
    {"numero": "FAC-003", "cliente": "Diana Gómez", "fecha": "2026-09-14", "total": 35.00, "estado": "Pendiente"}
]

@app.route('/')
def inicio():
    titulo_bienvenida = "Bienvenidos a Brilla Hermosa Mujer"
    return render_template('index.html', titulo=titulo_bienvenida)

# --- MÓDULO PRODUCTOS ---
@app.route('/productos')
def productos():
    cat_seleccionada = request.args.get('categoria', 'Todos')
    if cat_seleccionada != 'Todos':
        productos_filtrados = [p for p in PRODUCTOS if p['categoria'] == cat_seleccionada]
    else:
        productos_filtrados = PRODUCTOS
    return render_template('productos.html', productos=productos_filtrados, cat_seleccionada=cat_seleccionada)

@app.route('/productos/nuevo', methods=['GET', 'POST'])
def formulario_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        nuevo_p = {
            "id": len(PRODUCTOS) + 1,
            "nombre": form.nombre.data,
            "precio": form.precio.data,
            "stock": form.stock.data,
            "categoria": form.categoria.data,
            "descripcion": form.descripcion.data,
            "imagen": "img/Maquillaje.png"
        }
        PRODUCTOS.append(nuevo_p)
        flash('Producto guardado correctamente.', 'success')
        return redirect(url_for('productos'))
    return render_template('formulario_producto.html', form=form)

@app.route('/productos/eliminar/<int:producto_id>', methods=['POST'])
def eliminar_producto(producto_id):
    global PRODUCTOS
    PRODUCTOS = [p for p in PRODUCTOS if p['id'] != producto_id]
    flash('Producto eliminado correctamente.', 'warning')
    return redirect(url_for('productos'))

# --- MÓDULO CLIENTES ---
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

# --- MÓDULO PROVEEDORES ---
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

# --- MÓDULO FACTURACIÓN ---
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