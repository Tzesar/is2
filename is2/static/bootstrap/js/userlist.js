$("[name='usuario_activo']").bootstrapSwitch('onText', 'SI');
$("[name='usuario_activo']").bootstrapSwitch('offText', 'NO');

// Maneja los switches de activacion de un usuario
$('input[name="usuario_activo"]').on('switchChange.bootstrapSwitch', function(state) {
    $(this).bootstrapSwitch('disabled', true);

    var userId = $(this).attr("data_user_id");
    var url = $(this).attr("data_url") + "?xhr";
    var estadoActual = $(this).bootstrapSwitch('state');
    var csrftoken = $.cookie('csrftoken');
    var that = this;

    //alert(userId);

    $.ajax({
        url: url,
        context: document.body,
        type:"POST",
        crossDomain: false, // obviates need for sameOrigin test

        data:{usuarioModificado: userId, estadoNuevo: estadoActual},
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }

    })
        .done(function() {
            //alert("Done");
    })
        .always(function(response) {
            var userID = $(that).attr("data_user_id");
            //alert(userID);
            $(that).bootstrapSwitch('disabled', false);
    });
});

// Maneja el filtrado de los usuarios searchInput: id del input de texto
$("#searchInput").keyup(function () {
    //split the current value of searchInput
    var data = this.value.split(" ");
    //create a jquery object of the rows fbody: id del cuerpo de la tabla
    var jo = $("#fbody").find("tr");
    if (this.value == "") {
        jo.show();
        return;
    }
    //hide all the rows
    jo.hide();

    //Recusively filter the jquery object to get results.
    jo.filter(function (i, v) {
        var $t = $(this);
        for (var d = 0; d < data.length; ++d) {
            if ($t.is(":contains('" + data[d] + "')")) {
                return true;
            }
        }
        return false;
    //show the rows that match.
    }).show();
}).focus(function () {
    this.value = "";
    $(this).css({
        "color": "black"
    });
    $(this).unbind('focus');
}).css({
    "color": "#C0C0C0"
});