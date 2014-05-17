$('#id_usuarios').multiSelect({
    keepOrder: true,
    selectableHeader: "<h3>Usuarios disponibles</h3>",
    selectionHeader: "<h3>Usuarios a Asociar</h3>",
    dblClick: true,
    afterInit: function() {
        $("label[for='id_usuarios']").hide()
    }
})
