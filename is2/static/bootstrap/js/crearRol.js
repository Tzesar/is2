/*
 * Convierte los select normales en dobles selects con eventos para cambiar desde la lista de disponibles a
 * seleccionados y viceversa.
 * Ademas activa el selectbox para definir la fase donde se aplican ciertos permisos
 *
 */

$(document).ready(function() {

    $('.proyecto').multiSelect({
        keepOrder: true,
        selectableHeader: "<h3>Permisos Disponibles</h3>",
        selectionHeader: "<h3>Permisos Actuales</h3>"
    });

    $('.fase').multiSelect({
        keepOrder: true,
        selectableHeader: "<h3>Permisos Disponibles</h3>",
        selectionHeader: "<h3>Permisos Actuales</h3>"
    });

    $('#id_usuarios').multiSelect({
        keepOrder: true,
        selectableHeader: "<h3>Usuarios del Proyecto</h3>",
        selectionHeader: "<h3>Usuarios del Rol</h3>"
    });

    $("label[for='id_usuarios']").hide();

    $('#listaPermisosAcordeon').accordion({
        collapsible: true,
        active: false
    });
});