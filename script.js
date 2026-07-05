document.addEventListener("DOMContentLoaded", function() {
    const formProducto = document.getElementById("formProducto");
    const listaFavoritos = document.getElementById("listaFavoritos");
    const contadorProductos = document.getElementById("contadorProductos");
    const mensajeValidacion = document.getElementById("mensajeValidacion");
    const formContacto = document.getElementById("formContacto");
    const mensajeContacto = document.getElementById("mensajeContacto");

    let totalProductos = 0;
    const regexFormato = /^[A-ZÁÉÍÓÚÑ][a-záéíóúñü\s,.:;()]*$/;

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

    function limpiarValidacionInput(input, textoAyuda, mensajeOriginal) {
        input.classList.remove("is-invalid", "is-valid");
        textoAyuda.textContent = mensajeOriginal;
        textoAyuda.className = "form-text text-muted";
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
        
        el.addEventListener("input", () => limpiarValidacionInput(el, errEl, c.texto));
        el.addEventListener("blur", () => validarCampo(el, errEl, c.texto, c.min, c.nombre));
    });

    document.getElementById("prodCategoria").addEventListener("change", validarCategoria);
    document.getElementById("prodCategoria").addEventListener("blur", validarCategoria);
    document.getElementById("contEmail").addEventListener("blur", validarEmail);
    document.getElementById("contEmail").addEventListener("input", () => {
        const email = document.getElementById("contEmail");
        limpiarValidacionInput(email, document.getElementById("errContEmail"), "Debe ingresar un formato de correo válido (ejemplo@correo.com).");
    });

    formProducto.addEventListener("submit", function(event) {
        event.preventDefault();

        const vNom = validarCampo(document.getElementById("prodNombre"), document.getElementById("errProdNombre"), camposConfig[0].texto, 5, "nombre");
        const vCat = validarCategoria();
        const vDes = validarCampo(document.getElementById("prodDescripcion"), document.getElementById("errProdDescripcion"), camposConfig[1].texto, 10, "descripción");

        if (!vNom || !vCat || !vDes) {
            mensajeValidacion.className = "alert alert-danger d-block";
            mensajeValidacion.textContent = "Todos los campos obligatorios deben ser válidos antes de registrar.";
            return;
        }

        mensajeValidacion.className = "alert alert-success d-block";
        mensajeValidacion.textContent = "Producto registrado correctamente.";
        setTimeout(() => mensajeValidacion.className = "alert d-none", 3000);

        const col = document.createElement("div");
        col.className = "col-md-6 mb-3";
        col.innerHTML = `
            <div class="card card-dinamica h-100 p-3 shadow-sm">
                <span class="badge badge-categoria align-self-start">${document.getElementById("prodCategoria").value}</span>
                <h5 class="mt-2">${document.getElementById("prodNombre").value.trim()}</h5>
                <p class="text-muted small">${document.getElementById("prodDescripcion").value.trim()}</p>
                <button class="btn btn-danger btn-sm w-100 mt-auto btn-eliminar">Eliminar</button>
            </div>
        `;

        col.querySelector(".btn-eliminar").addEventListener("click", function() {
            col.remove();
            totalProductos--;
            contadorProductos.textContent = "Total productos: " + totalProductos;
        });

        listaFavoritos.appendChild(col);
        totalProductos++;
        contadorProductos.textContent = "Total productos: " + totalProductos;

        formProducto.reset();
        document.querySelectorAll("#formProducto input, #formProducto select, #formProducto textarea").forEach(el => el.classList.remove("is-valid"));
    });

    formContacto.addEventListener("submit", function(event) {
        event.preventDefault();

        const vNom = validarCampo(document.getElementById("contNombre"), document.getElementById("errContNombre"), camposConfig[2].texto, 0, "nombre");
        const vEma = validarEmail();
        const vAsu = validarCampo(document.getElementById("contAsunto"), document.getElementById("errContAsunto"), camposConfig[3].texto, 12, "asunto");
        const vMen = validarCampo(document.getElementById("contMensaje"), document.getElementById("errContMensaje"), camposConfig[4].texto, 25, "mensaje");

        if (!vNom || !vEma || !vAsu || !vMen) {
            mensajeContacto.className = "alert alert-danger d-block";
            mensajeContacto.textContent = "Por favor, corrija los errores en el formulario de contacto.";
            return;
        }

        mensajeContacto.className = "alert alert-success d-block";
        mensajeContacto.textContent = "¡Mensaje de contacto validado y enviado con éxito!";
        setTimeout(() => mensajeContacto.className = "alert d-none", 3000);

        formContacto.reset();
        document.querySelectorAll("#formContacto input, #formContacto textarea").forEach(el => el.classList.remove("is-valid"));
    });
});