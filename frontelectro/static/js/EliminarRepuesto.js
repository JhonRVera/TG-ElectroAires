function confirmarEliminacion(nombre, id) {
    if (confirm(`¿Estás seguro de eliminar el repuesto "${nombre}"?`)) {
        const form = document.getElementById('eliminar-form-' + id);
        form.submit();
    }
}