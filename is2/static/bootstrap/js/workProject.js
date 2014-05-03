// Inicializa los switches
$("[name='usuario_activo_proyecto']").bootstrapSwitch('onText', 'SI');
$("[name='usuario_activo_proyecto']").bootstrapSwitch('offText', 'NO');
$("[name='usuario_activo_proyecto']").bootstrapSwitch('size', 'mini');

// Maneja los switches de activacion de un usuario dentro de un proyecto
$('input[name="usuario_activo_proyecto"]').on('switchChange.bootstrapSwitch', function(state) {
    $(this).bootstrapSwitch('disabled', true);

    var idUsuario = $(this).attr("data_user_id");
    var url = $(this).attr("data_url") + "?xhr";
    var estadoNuevo = $(this).bootstrapSwitch('state');
    var csrftoken = $.cookie('csrftoken');
    var that = this;

    console.log(idUsuario);

    $.ajax({
        url: url,
        context: document.body,
        type:"POST",
        crossDomain: false, // obviates need for sameOrigin test

        data:{usuarioModificado: idUsuario, estadoNuevo: estadoNuevo},
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }

    })
        .done(function() {
            //alert("Done");
    })
        .always(function() {
            $(that).bootstrapSwitch('disabled', false);
    });
});