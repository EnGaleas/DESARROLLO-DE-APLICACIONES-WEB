document.addEventListener("DOMContentLoaded", function() {
    const formProducto = document.getElementById("formProducto");
    const prodNombre = document.getElementById("prodNombre");
    const prodCategoria = document.getElementById("prodCategoria");
    const prodDescripcion = document.getElementById("prodDescripcion");
    const listaFavoritos = document.getElementById("listaFavoritos");
    const contadorProductos = document.getElementById("contadorProductos");
    const mensajeValidacion = document.getElementById("mensajeValidacion");

    let totalProductos = 0;

    formProducto.addEventListener("submit", function(event) {
        event.preventDefault();

        const nombre = prodNombre.value.trim();
        const categoria = prodCategoria.value;
        const descripcion = prodDescripcion.value.trim();

        if (nombre === "" || categoria === "" || descripcion === "") {
            mensajeValidacion.className = "alert alert-danger";
            mensajeValidacion.textContent = "Todos los campos son obligatorios.";
            return;
        }

        mensajeValidacion.className = "alert alert-success";
        mensajeValidacion.textContent = "Producto registrado correctamente.";
        
        setTimeout(() => {
            mensajeValidacion.className = "alert d-none";
        }, 3000);

        const col = document.createElement("div");
        col.className = "col-md-6 mb-3";

        const card = document.createElement("div");
        card.className = "card card-dinamica h-100 p-3 shadow-sm";

        const badge = document.createElement("span");
        badge.className = "badge badge-categoria align-self-start";
        badge.textContent = categoria;

        const titulo = document.createElement("h5");
        titulo.className = "mt-2";
        titulo.textContent = nombre;

        const parrafo = document.createElement("p");
        parrafo.className = "text-muted small";
        parrafo.textContent = descripcion;

        const btnEliminar = document.createElement("button");
        btnEliminar.className = "btn btn-danger btn-sm w-100 mt-auto";
        btnEliminar.textContent = "Eliminar";

        btnEliminar.addEventListener("click", function() {
            col.remove();
            totalProductos--;
            contadorProductos.textContent = "Total productos: " + totalProductos;
        });

        card.appendChild(badge);
        card.appendChild(titulo);
        card.appendChild(parrafo);
        card.appendChild(btnEliminar);
        col.appendChild(card);
        listaFavoritos.appendChild(col);

        totalProductos++;
        contadorProductos.textContent = "Total productos: " + totalProductos;

        formProducto.reset();
    });
});