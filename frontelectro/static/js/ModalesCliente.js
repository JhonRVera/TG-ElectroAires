function cerrarCrearCliente(ventana) {
    const modal = document.getElementById(ventana);
    modal.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function() {
    const formCrearCliente = document.getElementById('formCrearCliente');
    formCrearCliente.addEventListener('submit', function(event) {
        event.preventDefault(); 
    });
});

function abrirCrearCliente() {
    const modal = document.getElementById('modalCrearUsuario');
    modal.style.display = 'block';
}
