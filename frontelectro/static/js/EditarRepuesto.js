function abrirModalEditar(id) {
    const modal = document.getElementById('modalEditar');
    modal.style.display = 'block';

    // Obtén los datos del producto correspondiente al ID desde la API
    const url = `https://electroaires.herokuapp.com/repuestos/${id}/`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            // Llena los campos del formulario con los datos del producto
            document.getElementById('nombre_r').value = data.r_nombre_repuesto;
            document.getElementById('cantidad').value = data.r_cantidad;
            document.getElementById('v_proveedor').value = data.r_valor_proveedor;
            document.getElementById('v_venta').value = data.r_valor_publico;
        })
        .catch(error => {
            console.error('Error al obtener los datos del producto:', error);
        });
}

function cerrarModalEditar() {
    const modal = document.getElementById('modalEditar');
    modal.style.display = 'none';
}

// Escucha el evento de envío del formulario para guardar los cambios
document.getElementById('editarForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Evita la recarga de la página por defecto

    const form = event.target;
    const url = form.action;
    const data = new FormData(form);

    // Envía la solicitud PUT a la API para actualizar los datos del producto
    fetch(url, {
        method: 'PUT',
        body: data
    })
        .then(response => {
            if (response.status === 200) {
                // Actualización exitosa, realiza las acciones necesarias (por ejemplo, cerrar el modal)
                cerrarModalEditar();
            } else {
                console.error('Error al guardar los cambios del producto:', response.status);
            }
        })
        .catch(error => {
            console.error('Error al guardar los cambios del producto:', error);
        });
});
