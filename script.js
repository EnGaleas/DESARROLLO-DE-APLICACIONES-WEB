document.addEventListener("DOMContentLoaded", () => {
    
    const formProducto = document.getElementById("formProducto");
    const inputNombre = document.getElementById("prodNombre");
    const selectCategoria = document.getElementById("prodCategoria");
    const txtDescripcion = document.getElementById("prodDescripcion");
    
    const listaFavoritos = document.getElementById("listaFavoritos");
    const contadorProductos = document.getElementById("contadorProductos");
    const mensajeValidacion = document.getElementById("mensajeValidacion");

    let totalProductos = 0;

    function actualizarContador() {
        contadorProductos.innerText = `Total productos: ${totalProductos}`;
    }

    formProducto.addEventListener("submit", (evento) => {
        evento.preventDefault();

        const nombre = inputNombre.value.trim();
        const categoria = selectCategoria.value;
        const descripcion = txtDescripcion.value.trim();

        if (nombre === "" || categoria === "" || descripcion === "") {
            mostrarMensaje("Por favor, completa todos los campos del formulario.", "alert-danger");
            return;
        }

        mensajeValidacion.classList.add("d-none");

        const colDiv = document.createElement("div");
        colDiv.classList.add("col-md-6", "mb-3");

        const cardDiv = document.createElement("div");
        cardDiv.classList.add("card-dinamica", "shadow-sm");

        const tituloElemento = document.createElement("h5");
        tituloElemento.innerText = nombre;

        const categoriaSpan = document.createElement("span");
        categoriaSpan.classList.add("badge", "badge-categoria");
        categoriaSpan.innerText = categoria;

        const descElemento = document.createElement("p");
        descElemento.innerText = descripcion;

        const btnEliminar = document.createElement("button");
        btnEliminar.classList.add("btn", "btn-danger", "btn-sm", "mt-2");
        btnEliminar.innerText = "❌ Eliminar";

        btnEliminar.addEventListener("click", () => {
            colDiv.remove();
            totalProductos--;
            actualizarContador();
        });

        cardDiv.appendChild(categoriaSpan);
        cardDiv.appendChild(tituloElemento);
        cardDiv.appendChild(descElemento);
        cardDiv.appendChild(btnEliminar);
        colDiv.appendChild(cardDiv);
        
        listaFavoritos.appendChild(colDiv);

        totalProductos++;
        actualizarContador();
        mostrarMensaje("✨ ¡Producto añadido con éxito!", "alert-success");

        formProducto.reset();
    });

    function mostrarMensaje(texto, claseBootstrap) {
        mensajeValidacion.innerText = texto;
        mensajeValidacion.className = `alert ${claseBootstrap} text-center py-2`;
        mensajeValidacion.classList.remove("d-none");
    }
});