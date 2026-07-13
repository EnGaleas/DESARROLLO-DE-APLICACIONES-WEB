document.addEventListener("DOMContentLoaded", function () {

    const catalogoProductos = [
        { id: 1, nombre: "Labiales", categoria: "Labios", descripcion: "Variedad de colores y acabados para cada ocasión.", disponible: true },
        { id: 2, nombre: "Gloss", categoria: "Labios", descripcion: "Brillo y suavidad para resaltar tus labios.", disponible: true },
        { id: 3, nombre: "Labial Líquido Mate", categoria: "Labios", descripcion: "Fórmula de larga duración con acabado mate uniforme.", disponible: true },
        { id: 4, nombre: "Bálsamo Labial", categoria: "Labios", descripcion: "Hidrata 24 horas y suaviza los labios resecos.", disponible: true },
        { id: 5, nombre: "Rímel", categoria: "Ojos", descripcion: "Mayor volumen y definición para tus pestañas.", disponible: true },
        { id: 6, nombre: "Sombras para Ojos", categoria: "Ojos", descripcion: "Diferentes tonos para cualquier estilo.", disponible: true },
        { id: 7, nombre: "Delineadores", categoria: "Ojos", descripcion: "Precisión y definición para tu mirada.", disponible: true },
        { id: 8, nombre: "Pestañas Postizas", categoria: "Ojos", descripcion: "Diseño natural para una mirada más intensa.", disponible: false },
        { id: 9, nombre: "Bases de Maquillaje", categoria: "Rostro", descripcion: "Cobertura uniforme para diferentes tipos de piel.", disponible: true },
        { id: 10, nombre: "Correctores", categoria: "Rostro", descripcion: "Ayudan a cubrir imperfecciones y ojeras.", disponible: false },
        { id: 11, nombre: "Rubores", categoria: "Rostro", descripcion: "Color natural para realzar tu rostro.", disponible: true },
        { id: 12, nombre: "Polvo Compacto", categoria: "Rostro", descripcion: "Fija el maquillaje y controla el brillo del rostro.", disponible: true },
        { id: 13, nombre: "Iluminador", categoria: "Rostro", descripcion: "Aporta un brillo suave y luminoso al rostro.", disponible: true },
        { id: 14, nombre: "Brochas", categoria: "Accesorios", descripcion: "Herramientas ideales para una aplicación profesional.", disponible: false },
        { id: 15, nombre: "Esponjas de Maquillaje", categoria: "Accesorios", descripcion: "Acabados suaves y naturales.", disponible: true }
    ];

    let inventarioProductos = [
        { nombre: "Labial Matte Cream", categoria: "Labios", descripcion: "Larga duracion con acabado aterciopelado." },
        { nombre: "Rimel Mega Vol", categoria: "Ojos", descripcion: "Mayor volumen y definicion desde la primera capa." },
        { nombre: "Base Hidratante Perfect", categoria: "Rostro", descripcion: "Cobertura uniforme ideal para pieles mixtas." }
    ];

    const promociones = [
        { texto: "Todos los miércoles 12% de descuento en todos los productos de maquillaje." },
        { texto: "En días festivos 20% de descuento en productos seleccionados." }
    ];

    let filtroActual = "todos";

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

    function mostrarToast(mensaje, tipo) {
        const toastEl = document.getElementById("toastGeneral");
        const toastMensaje = document.getElementById("toastMensaje");
        toastEl.classList.remove("bg-exito", "bg-error");
        toastEl.classList.add(tipo === "error" ? "bg-error" : "bg-exito");
        toastMensaje.textContent = mensaje;
        const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
        toast.show();
    }

    const regexFormato = /^[A-ZÁÉÍÓÚÑ][a-záéíóúñü0-9\s,.:;()]*$/;

    function validarCampo(input, elementoError, textoOriginal, minLength, nombreCampo) {
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
        } else if (!regexFormato.test(valor)) {
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
        textoAyuda.classList.remove("d-none");
        if (textoAyuda.textContent.trim() === "") {
            textoAyuda.textContent = mensajeOriginal;
        }
    }

    function renderizarCatalogo(filtro) {
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
                <div class="card-catalogo fade-in-card" style="animation-delay:${index * 0.05}s">
                    <h5>${producto.nombre}</h5>
                    <p class="mt-2">${producto.descripcion}</p>
                    <span class="badge-estado ${producto.disponible ? "badge-disponible" : "badge-agotado"}">
                        ${producto.disponible ? "Disponible" : "Agotado"}
                    </span>
                </div>
            `;
            catalogoContenedor.appendChild(col);
        });
    }

    botonesFiltro.forEach(boton => {
        boton.addEventListener("click", function () {
            botonesFiltro.forEach(b => b.classList.remove("active"));
            this.classList.add("active");
            filtroActual = this.getAttribute("data-categoria");
            renderizarCatalogo(filtroActual);
        });
    });

    function renderizarInventario() {
        listaFavoritos.innerHTML = "";

        if (inventarioProductos.length === 0) {
            listaFavoritos.innerHTML = `
                <div class="col-12 text-center p-4">
                    <div class="alert alert-warning">No hay productos registrados en el inventario actual.</div>
                </div>
            `;
            contadorProductos.textContent = "Total productos: 0";
            actualizarEstadisticas();
            return;
        }

        inventarioProductos.forEach((producto, index) => {
            const col = document.createElement("div");
            col.className = "col-md-6 mb-3";
            col.innerHTML = `
                <div class="card card-dinamica h-100 p-3 shadow-sm fade-in-card">
                    <span class="badge badge-categoria align-self-start">${producto.categoria}</span>
                    <h5 class="mt-2">${producto.nombre}</h5>
                    <p class="text-muted small text-start">${producto.descripcion}</p>
                    <button class="btn btn-danger btn-sm w-100 mt-auto btn-eliminar" data-index="${index}">Eliminar</button>
                </div>
            `;
            listaFavoritos.appendChild(col);
        });

        contadorProductos.textContent = "Total productos: " + inventarioProductos.length;

        document.querySelectorAll(".btn-eliminar").forEach(boton => {
            boton.addEventListener("click", function () {
                const idx = this.getAttribute("data-index");
                inventarioProductos.splice(idx, 1);
                renderizarInventario();
                mostrarToast("Producto eliminado del inventario.", "error");
            });
        });

        actualizarEstadisticas();
    }

    function actualizarEstadisticas() {
        const total = catalogoProductos.length;
        const disponibles = catalogoProductos.filter(p => p.disponible).length;
        const agotados = total - disponibles;

        document.getElementById("statTotal").textContent = total;
        document.getElementById("statDisponibles").textContent = disponibles;
        document.getElementById("statAgotados").textContent = agotados;
        document.getElementById("statRegistrados").textContent = inventarioProductos.length;
    }

    function renderizarPromociones() {
        listaPromociones.innerHTML = "";
        promociones.forEach(promo => {
            const li = document.createElement("li");
            li.textContent = promo.texto;
            listaPromociones.appendChild(li);
        });
    }

    const camposConfig = [
        { id: "prodNombre", errId: "errProdNombre", texto: "Debe tener mínimo 5 caracteres, iniciar con Mayúscula y el resto en minúsculas.", min: 5, nombre: "nombre" },
        { id: "prodDescripcion", errId: "errProdDescripcion", texto: "Debe iniciar con Mayúscula, el resto en minúsculas y tener mínimo 10 caracteres.", min: 10, nombre: "descripción" },
        { id: "contNombre", errId: "errContNombre", texto: "El nombre debe iniciar con Mayúscula y el resto en minúsculas.", min: 0, nombre: "nombre" },
        { id: "contAsunto", errId: "errContAsunto", texto: "El asunto debe iniciar con Mayúscula, el resto en minúsculas y tener mínimo 12 caracteres.", min: 12, nombre: "asunto" },
        { id: "contMensaje", errId: "errContMensaje", texto: "El mensaje debe tener un mínimo de 25 caracteres.", min: 25, nombre: "mensaje" }
    ];

    camposConfig.forEach(c => {
        const el = document.getElementById(c.id);
        const errEl = document.getElementById(c.errId);

        el.addEventListener("focus", () => mostrarPista(errEl, c.texto));
        el.addEventListener("input", () => validarCampo(el, errEl, c.texto, c.min, c.nombre));
        el.addEventListener("blur", () => {
            validarCampo(el, errEl, c.texto, c.min, c.nombre);
            errEl.classList.add("d-none");
        });
    });

    const prodCategoria = document.getElementById("prodCategoria");
    const errProdCategoria = document.getElementById("errProdCategoria");
    prodCategoria.addEventListener("focus", () => mostrarPista(errProdCategoria, "Debe seleccionar una categoría para el producto."));
    prodCategoria.addEventListener("change", validarCategoria);
    prodCategoria.addEventListener("blur", () => {
        validarCategoria();
        errProdCategoria.classList.add("d-none");
    });

    const contEmail = document.getElementById("contEmail");
    const errContEmail = document.getElementById("errContEmail");
    contEmail.addEventListener("focus", () => mostrarPista(errContEmail, "Debe ingresar un formato de correo válido (ejemplo@correo.com)."));
    contEmail.addEventListener("input", validarEmail);
    contEmail.addEventListener("blur", () => {
        validarEmail();
        errContEmail.classList.add("d-none");
    });

    formProducto.addEventListener("submit", function (event) {
        event.preventDefault();

        const vNom = validarCampo(document.getElementById("prodNombre"), document.getElementById("errProdNombre"), camposConfig[0].texto, 5, "nombre");
        const vCat = validarCategoria();
        const vDes = validarCampo(document.getElementById("prodDescripcion"), document.getElementById("errProdDescripcion"), camposConfig[1].texto, 10, "descripción");

        if (!vNom || !vCat || !vDes) {
            clearTimeout(window.prodTimeout);
            mensajeValidacion.className = "alert alert-danger d-block";
            mensajeValidacion.textContent = "Todos los campos obligatorios deben ser válidos antes de registrar.";
            mostrarToast("Revisa los campos marcados en rojo.", "error");
            return;
        }

        clearTimeout(window.prodTimeout);
        mensajeValidacion.className = "alert alert-success d-block";
        mensajeValidacion.textContent = "Producto registrado correctamente.";
        window.prodTimeout = setTimeout(() => mensajeValidacion.className = "alert d-none", 3000);

        const nuevoProd = {
            nombre: document.getElementById("prodNombre").value.trim(),
            categoria: document.getElementById("prodCategoria").value,
            descripcion: document.getElementById("prodDescripcion").value.trim()
        };

        inventarioProductos.push(nuevoProd);
        renderizarInventario();
        mostrarToast(`"${nuevoProd.nombre}" fue agregado al inventario.`, "exito");

        formProducto.reset();
        document.querySelectorAll("#formProducto input, #formProducto select, #formProducto textarea").forEach(el => el.classList.remove("is-valid"));
    });

    formContacto.addEventListener("submit", function (event) {
        event.preventDefault();

        const vNom = validarCampo(document.getElementById("contNombre"), document.getElementById("errContNombre"), camposConfig[2].texto, 0, "nombre");
        const vEma = validarEmail();
        const vAsu = validarCampo(document.getElementById("contAsunto"), document.getElementById("errContAsunto"), camposConfig[3].texto, 12, "asunto");
        const vMen = validarCampo(document.getElementById("contMensaje"), document.getElementById("errContMensaje"), camposConfig[4].texto, 25, "mensaje");

        if (!vNom || !vEma || !vAsu || !vMen) {
            clearTimeout(window.contTimeout);
            mensajeContacto.className = "alert alert-danger d-block";
            mensajeContacto.textContent = "Por favor, corrija los errores en el formulario de contacto.";
            mostrarToast("Revisa los campos del formulario de contacto.", "error");
            return;
        }

        clearTimeout(window.contTimeout);
        mensajeContacto.className = "alert alert-success d-block";
        mensajeContacto.textContent = "¡Mensaje de contacto validado y enviado con éxito!";
        window.contTimeout = setTimeout(() => mensajeContacto.className = "alert d-none", 3000);
        mostrarToast("¡Gracias por escribirnos! Te responderemos pronto.", "exito");

        formContacto.reset();
        document.querySelectorAll("#formContacto input, #formContacto textarea").forEach(el => el.classList.remove("is-valid"));
    });

    const enlacesNav = document.querySelectorAll(".nav-link");

    const observador = new IntersectionObserver((entradas) => {
        entradas.forEach(entrada => {
            if (entrada.isIntersecting) {
                const id = entrada.target.getAttribute("id");
                enlacesNav.forEach(link => {
                    link.classList.toggle("active", link.getAttribute("href") === `#${id}`);
                });
            }
        });
    }, { rootMargin: "-40% 0px -50% 0px" });

    document.querySelectorAll("main section[id]").forEach(sec => observador.observe(sec));

    window.addEventListener("scroll", () => {
        if (window.scrollY > 300) {
            btnSubir.classList.add("mostrar");
        } else {
            btnSubir.classList.remove("mostrar");
        }
    });

    btnSubir.addEventListener("click", () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });

    renderizarCatalogo(filtroActual);
    renderizarInventario();
    renderizarPromociones();
});