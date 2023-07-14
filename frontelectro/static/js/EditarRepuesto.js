function abrirModalEditar(id) {
    const modal = document.getElementById('modalEditar');
    modal.style.display = 'block';

}

function cerrarModalEditar() {
    const modal = document.getElementById('modalEditar');
    modal.style.display = 'none';
}
document.getElementById('editarForm').addEventListener('submit', function(event) {
    event.preventDefault(); 
});
