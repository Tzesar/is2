$(document).ready(function() {

    $('#id_items').multiSelect({
        keepOrder: true,
        selectableHeader: "<h3>Items en LB</h3>",
        selectionHeader: "<h3>Items en Solicitud</h3>"
    });
});
