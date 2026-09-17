document.addEventListener("DOMContentLoaded", function () {

    const catalogoProductos = [
        { id: 1, nombre: "Labiales", categoria: "Labios", descripcion: "Variedad de colores y acabados para cada ocasión.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 5.50 },
        { id: 2, nombre: "Gloss", categoria: "Labios", descripcion: "Brillo y suavidad para resaltar tus labios.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 4.00 },
        { id: 3, nombre: "Labial líquido mate", categoria: "Labios", descripcion: "Fórmula de larga duración con acabado mate uniforme.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 6.50 },
        { id: 4, nombre: "Bálsamo labial", categoria: "Labios", descripcion: "Hidrata 24 horas y suaviza los labios resecos.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 3.50 },
        { id: 5, nombre: "Rímel", categoria: "Ojos", descripcion: "Mayor volumen y definición para tus pestañas.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 6.00 },
        { id: 6, nombre: "Sombras para ojos", categoria: "Ojos", descripcion: "Diferentes tonos para cualquier estilo.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 7.50 },
        { id: 7, nombre: "Delineadores", categoria: "Ojos", descripcion: "Precisión y definición para tu mirada.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 4.50 },
        { id: 8, nombre: "Pestañas postizas", categoria: "Ojos", descripcion: "Diseño natural para una mirada más intensa.", disponible: false, marca: "Brilla Hermosa Mujer", precio: 5.00 },
        { id: 9, nombre: "Bases de maquillaje", categoria: "Rostro", descripcion: "Cobertura uniforme para diferentes tipos de piel.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 9.00 },
        { id: 10, nombre: "Correctores", categoria: "Rostro", descripcion: "Ayudan a cubrir imperfecciones y ojeras.", disponible: false, marca: "Brilla Hermosa Mujer", precio: 5.50 },
        { id: 11, nombre: "Rubores", categoria: "Rostro", descripcion: "Color natural para realzar tu rostro.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 6.00 },
        { id: 12, nombre: "Polvo compacto", categoria: "Rostro", descripcion: "Fija el maquillaje y controla el brillo del rostro.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 7.00 },
        { id: 13, nombre: "Iluminador", categoria: "Rostro", descripcion: "Aporta un brillo suave y luminoso al rostro.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 6.50 },
        { id: 14, nombre: "Brochas", categoria: "Accesorios", descripcion: "Herramientas ideales para una aplicación profesional.", disponible: false, marca: "Brilla Hermosa Mujer", precio: 4.00 },
        { id: 15, nombre: "Esponjas de maquillaje", categoria: "Accesorios", descripcion: "Acabados suaves y naturales.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 2.50 },
        { id: 16, nombre: "Delineador de labios", categoria: "Labios", descripcion: "Define el contorno y mejora el acabado del labial.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 4.00 },
        { id: 17, nombre: "Tinta para labios", categoria: "Labios", descripcion: "Color ligero con mayor duración.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 5.50 },
        { id: 18, module: "Aceite labial", nombre: "Aceite labial", categoria: "Labios", descripcion: "Hidratación y brillo para los labios.", disponible: false, marca: "Brilla Hermosa Mujer", precio: 4.50 },
        { id: 19, nombre: "Set de labiales", categoria: "Labios", descripcion: "Combinación de diferentes tonos en un solo producto.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 12.00 },
        { id: 20, nombre: "Lápiz de cejas", categoria: "Ojos", descripcion: "Permite rellenar y definir las cejas.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 3.50 },
        { id: 21, nombre: "Gel para cejas", categoria: "Ojos", descripcion: "Mantiene las cejas peinadas y ordenadas.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 4.00 },
        { id: 22, nombre: "Paleta de sombras", categoria: "Ojos", descripcion: "Incluye varios tonos para crear diferentes maquillajes.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 10.00 },
        { id: 23, nombre: "Primer de ojos", categoria: "Ojos", descripcion: "Ayuda a fijar las sombras y aumentar su duración.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 6.00 },
        { id: 24, nombre: "Máscara de cejas", categoria: "Ojos", descripcion: "Aporta color y volumen a las cejas.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 5.00 },
        { id: 25, nombre: "Primer facial", categoria: "Rostro", descripcion: "Prepara la piel antes del maquillaje y mejora el acabado.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 8.00 },
        { id: 26, nombre: "Contorno facial", categoria: "Rostro", descripcion: "Ayuda a definir las facciones del rostro.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 7.50 },
        { id: 27, nombre: "Bronceador", categoria: "Rostro", descripcion: "Aporta un tono cálido y natural a la piel.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 7.00 },
        { id: 28, nombre: "Fijador de maquillaje", categoria: "Rostro", descripcion: "Prolonga la duración del maquillaje durante el día.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 6.50 },
        { id: 29, nombre: "Bb cream", categoria: "Rostro", descripcion: "Combina hidratación y cobertura ligera.", disponible: false, marca: "Brilla Hermosa Mujer", precio: 9.50 },
        { id: 30, nombre: "Corrector de color", categoria: "Rostro", descripcion: "Ayuda a neutralizar manchas y tonos desiguales.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 6.00 },
        { id: 31, nombre: "Agua micelar", categoria: "Rostro", descripcion: "Limpia y prepara la piel antes del maquillaje.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 5.50 },
        { id: 32, nombre: "Crema hidratante facial", categoria: "Rostro", descripcion: "Mantiene la piel suave e hidratada.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 8.50 },
        { id: 33, nombre: "Protector solar facial", categoria: "Rostro", descripcion: "Protege la piel antes de aplicar maquillaje.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 9.00 },
        { id: 34, nombre: "Exfoliante facial", categoria: "Rostro", descripcion: "Ayuda a eliminar impurezas y células muiertas.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 6.50 },
        { id: 35, nombre: "Kit de brochas", categoria: "Accesorios", descripcion: "Incluye diferentes tamaños para una aplicación completa.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 14.00 },
        { id: 36, nombre: "Pinzas para cejas", categoria: "Accesorios", descripcion: "Facilitan el cuidado y definición de las cejas.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 3.00 },
        { id: 37, nombre: "Sacapuntas cosmético", categoria: "Accesorios", descripcion: "Ideal para lápices de ojos y labios.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 2.00 },
        { id: 38, nombre: "Organizador de maquillaje", categoria: "Accesorios", descripcion: "Permite guardar los productos de forma ordenada.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 11.00 },
        { id: 39, nombre: "Neceser de maquillaje", categoria: "Accesorios", descripcion: "Facilita transportar productos de belleza.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 9.50 },
        { id: 40, nombre: "Espejo de maquillaje", categoria: "Accesorios", descripcion: "Accesorio práctico para aplicar maquillaje.", disponible: true, marca: "Brilla Hermosa Mujer", precio: 6.00 }
    ];

    let inventarioProductos = [
        { nombre: "Labial Matte Cream", categoria: "Labios", descripcion: "Larga duracion con acabado aterciopelado." },
        { nombre: "Rimel Mega Vol", categoria: "Ojos", descripcion: "Mayor volumen y definicion desde la primera capa." },
        { fontawesome: "Base Hidratante Perfect", nombre: "Base Hidratante Perfect", categoria: "Rostro", descripcion: "Cobertura uniforme ideal para pieles mixtas." }
    ];

    const promociones = [
        { texto: "Todos los miércoles 12% de descuento en todos los productos de maquillaje." },
        { texto: "En días festivos 20% de descuento en productos seleccionados." }
    ];

    let filtroActual = "todos";
    let indiceAEliminar = null;

    const formProducto = document.getElementById("formProducto");
    const listaFavoritos = document.getElementById("listaFavoritos");
    const contadorProductos = document.getElementById("contadorProductos");
    const mensajeValidacion = document.getElementById("mensajeValidacion");
    
    const formContacto = document.getElementById("formContacto");
    const mensajeContacto = document.getElementById("mensajeContacto");
    
    const catalogoContenedor = document.getElementById("catalogoProductos");
    const botonesFiltro = document.querySelectorAll(".btn-filtro");
    const listaPromociones = document.getElementById("listaPromociones");
    const btnSubir = document.getElementById("btnSubir");

    const modalEliminarEl = document.getElementById("modalEliminar");
    const btnConfirmarEliminar = document.getElementById("btnConfirmarEliminar");
    const contenedorSpinner = document.getElementById("contenedorSpinner");

    function mostrarToast(mensaje, tipo) {
        const toastEl = document.getElementById("toastGeneral");
        const toastMensaje = document.getElementById("toastMensaje");
        if (!toastEl) return;
        toastEl.classList.remove("bg-success", "bg-danger");
        toastEl.classList.add(tipo === "error" ? "bg-danger" : "bg-success");
        toastMensaje.textContent = mensaje;
        const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
        toast.show();
    }

    const regexFormato = /^[A-ZÁÉÍÓÚÑ][a-záéíóúñü0-9\s,.:;()]*$/;
    const regexNombreCompleto = /^[A-ZÁÉÍÓÚÑ][a-záéíóúñ]*(\s[A-ZÁÉÍÓÚÑ][a-záéíúñ]*)*$/;

    function validarCampo(input, elementoError, textoOriginal, minLength, nombreCampo, regex = regexFormato) {
        if (!input || !elementoError) return false;
        const valor = input.value.trim();

        if (valor === "") {
            elementoError.textContent = `El campo ${nombreCampo} es obligatorio.`;
            elementoError.className = "form-text text-danger";
            input.classList.add("is-invalid");
            input.classList.remove("is-valid");
            return false;
        } else if (minLength && valor.length < minLength) {
            elementoError.textContent = `Incorrecto. Falta caracteres (Mínimo deben ser ${minLength}).`;
            elementoError.className = "form-text text-danger";
            input.classList.add("is-invalid");
            input.classList.remove("is-valid");
            return false;
        } else if (!regex.test(valor)) {
            elementoError.textContent = "Incorrecto. Corrija el formato: Debe iniciar con una Mayúscula y el resto en minúsculas.";
            elementoError.className = "form-text text-danger";
            input.classList.add("is-invalid");
            input.classList.remove("is-valid");
            return false;
        } else {
            elementoError.textContent = textoOriginal;
            elementoError.className = "form-text text-muted";
            input.classList.remove("is-invalid");
            input.classList.add("is-valid");
            return true;
        }
    }

    function validarEmail() {
        const email = document.getElementById("contEmail");
        const errContEmail = document.getElementById("errContEmail");
        if (!email || !errContEmail) return false;
        const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (email.value.trim() === "") {
            errContEmail.textContent = "El campo correo electrónico es obligatorio.";
            errContEmail.className = "form-text text-danger";
            email.classList.add("is-invalid");
            return false;
        } else if (!regexEmail.test(email.value.trim())) {
            errContEmail.textContent = "Incorrecto. Correo electrónico inválido.";
            errContEmail.className = "form-text text-danger";
            email.classList.add("is-invalid");
            return false;
        } else {
            errContEmail.textContent = "Debe ingresar un formato de correo válido (ejemplo@correo.com).";
            errContEmail.className = "form-text text-muted";
            email.classList.remove("is-invalid");
            email.classList.add("is-valid");
            return true;
        }
    }

    function validarCategoria() {
        const cat = document.getElementById("prodCategoria");
        const errCat = document.getElementById("errProdCategoria");
        if (!cat || !errCat) return false;
        if (cat.value === "") {
            errCat.textContent = "Incorrecto. No cumple con lo solicitado. Debe elegir una categoría.";
            errCat.className = "form-text text-danger";
            cat.classList.add("is-invalid");
            return false;
        } else {
            errCat.textContent = "Debe seleccionar una categoría para el producto.";
            errCat.className = "form-text text-muted";
            cat.classList.remove("is-invalid");
            cat.classList.add("is-valid");
            return true;
        }
    }

    function mostrarPista(textoAyuda, mensajeOriginal) {
        if (!textoAyuda) return;
        textoAyuda.classList.remove("d-none");
        if (textoAyuda.textContent.trim() === "") {
            textoAyuda.textContent = mensajeOriginal;
        }
    }

    function renderizarCatalogo(filtro) {
        if (!catalogoContenedor) return;
        catalogoContenedor.innerHTML = "";

        const productosFiltrados = filtro === "todos"
            ? catalogoProductos
            : catalogoProductos.filter(p => p.categoria === filtro);

        if (productosFiltrados.length === 0) {
            catalogoContenedor.innerHTML = `
                <div class="col-12 text-center p-4">
                    <div class="alert alert-warning">No hay productos disponibles en esta categoría por el momento.</div>
                </div>`;
            return;
        }

        productosFiltrados.forEach((producto, index) => {
            const col = document.createElement("div");
            col.className = "col-md-4 col-sm-6 mb-4";
            col.innerHTML = `
                <div class="card card-catalogo fade-in-card ${producto.disponible ? '' : 'card-catalogo-agotada'}" style="animation-delay:${index * 0.05}s">
                    <h5>${producto.nombre}</h5>
                    <p class="mt-2 text-muted small">${producto.descripcion}</p>
                    <div class="d-flex justify-content-between align-items-center mt-auto pt-2">
                        <span class="fw-bold text-purple">$${producto.precio.toFixed(2)}</span>
                        <span class="badge-estado ${producto.disponible ? 'badge-disponible' : 'badge-agotado'}">
                            ${producto.disponible ? "Disponible" : "Agotado"}
                        </span>
                    </div>
                </div>
            `;
            catalogoContenedor.appendChild(col);
        });
    }

    if (botonesFiltro) {
        botonesFiltro.forEach(boton => {
            boton.addEventListener("click", function () {
                botonesFiltro.forEach(b => b.classList.remove("active"));
                this.classList.add("active");
                filtroActual = this.getAttribute("data-categoria");
                renderizarCatalogo(filtroActual);
            });
        });
    }

    function renderizarInventario() {
        if (!listaFavoritos) return;
        listaFavoritos.innerHTML = "";

        if (inventarioProductos.length === 0) {
            listaFavoritos.innerHTML = `
                <div class="col-12 text-center p-4">
                    <div class="alert alert-warning">No hay productos registrados en el inventario actual.</div>
                </div>
            `;
            if (contadorProductos) contadorProductos.textContent = "Total productos: 0";
            actualizarEstadisticas();
            return;
        }

        inventarioProductos.forEach((producto, index) => {
            const col = document.createElement("div");
            col.className = "col-md-6 mb-3";
            col.innerHTML = `
                <div class="card card-dinamica h-100 p-3 shadow-sm fade-in-card">
                    <span class="badge bg-purple align-self-start">${producto.categoria}</span>
                    <h5 class="mt-2">${producto.nombre}</h5>
                    <p class="text-muted small text-start">${producto.descripcion}</p>
                    <button class="btn btn-danger btn-sm w-100 mt-auto btn-eliminar" data-index="${index}">Eliminar</button>
                </div>
            `;
            listaFavoritos.appendChild(col);
        });

        if (contadorProductos) contadorProductos.textContent = "Total productos: " + inventarioProductos.length;

        document.querySelectorAll(".btn-eliminar").forEach(boton => {
            boton.addEventListener("click", function () {
                indiceAEliminar = this.getAttribute("data-index");
                if (modalEliminarEl) {
                    const mEliminar = new bootstrap.Modal(modalEliminarEl);
                    mEliminar.show();
                }
            });
        });

        actualizarEstadisticas();
    }

    if (btnConfirmarEliminar) {
        btnConfirmarEliminar.addEventListener("click", function () {
            if (indiceAEliminar !== null) {
                const eliminado = inventarioProductos.splice(indiceAEliminar, 1);
                renderizarInventario();
                if (modalEliminarEl) {
                    bootstrap.Modal.getInstance(modalEliminarEl).hide();
                }
                mostrarToast(`"${eliminado[0].nombre}" fue eliminado del inventario.`, "error");
                indiceAEliminar = null;
            }
        });
    }

    function actualizarEstadisticas() {
        const total = catalogoProductos.length;
        const disponibles = catalogoProductos.filter(p => p.disponible).length;
        const agotados = total - disponibles;

        const statTotal = document.getElementById("statTotal");
        const statDisponibles = document.getElementById("statDisponibles");
        const statAgotados = document.getElementById("statAgotados");
        const statRegistrados = document.getElementById("statRegistrados");

        if (statTotal) statTotal.textContent = total;
        if (statDisponibles) statDisponibles.textContent = disponibles;
        if (statAgotados) statAgotados.textContent = agotados;
        if (statRegistrados) statRegistrados.textContent = inventarioProductos.length;
    }

    function renderizarPromociones() {
        if (!listaPromociones) return;
        listaPromociones.innerHTML = "";
        promociones.forEach(promo => {
            const li = document.createElement("li");
            li.textContent = promo.texto;
            listaPromociones.appendChild(li);
        });
    }

    const camposConfig = [
        { id: "prodNombre", errId: "errProdNombre", texto: "Debe tener mínimo 5 caracteres, iniciar con Mayúscula y el resto en minúsculas.", min: 5, nombre: "nombre", regex: regexFormato },
        { id: "prodDescripcion", errId: "errProdDescripcion", texto: "Debe iniciar con Mayúscula, el resto en minúsculas y tener mínimo 10 caracteres.", min: 10, nombre: "descripción", regex: regexFormato },
        { id: "contNombre", errId: "errContNombre", texto: "El nombre debe iniciar con Mayúscula y el resto en minúsculas.", min: 0, nombre: "nombre", regex: regexNombreCompleto },
        { id: "contAsunto", errId: "errContAsunto", texto: "El asunto debe iniciar con Mayúscula, el resto en minúsculas y tener mínimo 8 caracteres.", min: 8, nombre: "asunto", regex: regexFormato },
        { id: "contMensaje", errId: "errContMensaje", texto: "El mensaje debe iniciar con Mayúscula, el resto en minúsculas y tener mínimo 15 caracteres.", min: 15, nombre: "mensaje", regex: regexFormato }
    ];

    camposConfig.forEach(c => {
        const el = document.getElementById(c.id);
        const errEl = document.getElementById(c.errId);
        if (!el || !errEl) return;

        el.addEventListener("focus", () => mostrarPista(errEl, c.texto));
        el.addEventListener("input", () => validarCampo(el, errEl, c.texto, c.min, c.nombre, c.regex));
        el.addEventListener("blur", () => {
            validarCampo(el, errEl, c.texto, c.min, c.nombre, c.regex);
            errEl.classList.add("d-none");
        });
    });

    const prodCategoria = document.getElementById("prodCategoria");
    const errProdCategoria = document.getElementById("errProdCategoria");
    if (prodCategoria && errProdCategoria) {
        prodCategoria.addEventListener("focus", () => mostrarPista(errProdCategoria, "Debe seleccionar una categoría para el producto."));
        prodCategoria.addEventListener("change", validarCategoria);
        prodCategoria.addEventListener("blur", () => {
            validarCategoria();
            errProdCategoria.classList.add("d-none");
        });
    }

    const contEmail = document.getElementById("contEmail");
    const errContEmail = document.getElementById("errContEmail");
    if (contEmail && errContEmail) {
        contEmail.addEventListener("focus", () => mostrarPista(errContEmail, "Debe ingresar un formato de correo válido (ejemplo@correo.com)."));
        contEmail.addEventListener("input", validarEmail);
        contEmail.addEventListener("blur", () => {
            validarEmail();
            errContEmail.classList.add("d-none");
        });
    }

    if (formProducto) {
        formProducto.addEventListener("submit", function (event) {
            event.preventDefault();

            const vNom = validarCampo(document.getElementById("prodNombre"), document.getElementById("errProdNombre"), camposConfig[0].texto, 5, "nombre", regexFormato);
            const vCat = validarCategoria();
            const vDes = validarCampo(document.getElementById("prodDescripcion"), document.getElementById("errProdDescripcion"), camposConfig[1].texto, 10, "descripción", regexFormato);

            if (!vNom || !vCat || !vDes) {
                if (mensajeValidacion) {
                    clearTimeout(window.prodTimeout);
                    mensajeValidacion.className = "alert alert-danger d-block";
                    mensajeValidacion.textContent = "Todos los campos obligatorios deben ser válidos antes de registrar.";
                }
                mostrarToast("Revisa los campos marcados en rojo.", "error");
                return;
            }

            if (contenedorSpinner) contenedorSpinner.classList.remove("d-none");
            if (mensajeValidacion) mensajeValidacion.className = "alert d-none";

            setTimeout(() => {
                if (contenedorSpinner) contenedorSpinner.classList.add("d-none");

                const nuevoProd = {
                    nombre: document.getElementById("prodNombre").value.trim(),
                    categoria: document.getElementById("prodCategoria").value,
                    descripcion: document.getElementById("prodDescripcion").value.trim()
                };

                inventarioProductos.push(nuevoProd);
                renderizarInventario();

                if (mensajeValidacion) {
                    clearTimeout(window.prodTimeout);
                    mensajeValidacion.className = "alert alert-success d-block";
                    mensajeValidacion.textContent = "Producto registrado correctamente.";
                    window.prodTimeout = setTimeout(() => mensajeValidacion.className = "alert d-none", 3000);
                }

                mostrarToast(`"${nuevoProd.nombre}" fue agregado al inventario.`, "exito");

                formProducto.reset();
                document.querySelectorAll("#formProducto .form-control, #formProducto .form-select").forEach(el => el.classList.remove("is-valid"));
            }, 1500);
        });
    }

    if (formContacto) {
        formContacto.addEventListener("submit", function (event) {
            event.preventDefault();

            const vNom = validarCampo(document.getElementById("contNombre"), document.getElementById("errContNombre"), camposConfig[2].texto, 0, "nombre", regexNombreCompleto);
            const vEma = validarEmail();
            const vAsu = validarCampo(document.getElementById("contAsunto"), document.getElementById("errContAsunto"), camposConfig[3].texto, 12, "asunto", regexFormato);
            const vMen = validarCampo(document.getElementById("contMensaje"), document.getElementById("errContMensaje"), camposConfig[4].texto, 25, "mensaje", regexFormato);

            if (!vNom || !vEma || !vAsu || !vMen) {
                if (mensajeContacto) {
                    clearTimeout(window.contTimeout);
                    mensajeContacto.className = "alert alert-danger d-block";
                    mensajeContacto.textContent = "Por favor, corrija los errores en el formulario de contacto.";
                }
                mostrarToast("Revisa los campos del formulario de contacto.", "error");
                return;
            }

            if (contenedorSpinner) contenedorSpinner.classList.remove("d-none");
            if (mensajeContacto) mensajeContacto.className = "alert d-none";

            setTimeout(() => {
                if (contenedorSpinner) contenedorSpinner.classList.add("d-none");

                if (mensajeContacto) {
                    clearTimeout(window.contTimeout);
                    mensajeContacto.className = "alert alert-success d-block";
                    mensajeContacto.textContent = "¡Mensaje de contacto validado y enviado con éxito!";
                    window.contTimeout = setTimeout(() => mensajeContacto.className = "alert d-none", 3000);
                }
                mostrarToast("¡Gracias por escribirnos! Te responderemos pronto.", "exito");

                formContacto.reset();
                document.querySelectorAll("#formContacto .form-control").forEach(el => el.classList.remove("is-valid"));
            }, 1500);
        });
    }

    const secciones = document.querySelectorAll("main > section");
    const enlacesNav = document.querySelectorAll(".navbar-nav .nav-link");

    window.addEventListener("scroll", () => {
        if (btnSubir) {
            if (window.scrollY > 300) {
                btnSubir.classList.add("mostrar");
            } else {
                btnSubir.classList.remove("mostrar");
            }
        }

        let seccionActual = "";
        secciones.forEach(seccion => {
            const seccionTop = seccion.offsetTop;
            const seccionHeight = seccion.clientHeight;
            if (window.scrollY >= (seccionTop - 150)) {
                seccionActual = seccion.getAttribute("id");
            }
        });

        enlacesNav.forEach(enlace => {
            enlace.classList.remove("active");
            if (enlace.getAttribute("href") === `#${seccionActual}`) {
                enlace.classList.add("active");
            }
        });
    });

    if (btnSubir) {
        btnSubir.addEventListener("click", () => {
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }

    enlacesNav.forEach(enlace => {
        enlace.addEventListener("click", () => {
            const menuColapsable = document.getElementById("menu");
            if (menuColapsable && menuColapsable.classList.contains("show")) {
                const bCollapse = bootstrap.Collapse.getInstance(menuColapsable);
                if (bCollapse) bCollapse.hide();
            }
        });
    });

    renderizarCatalogo(filtroActual);
    renderizarInventario();
    renderizarPromociones();
});