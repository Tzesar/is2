// Inicializa los switches
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
        .always(function() {
            $(that).bootstrapSwitch('disabled', false);
    });
});

// Muestra el campo searchInput cuando el mouse pasa sobre el icono searchIcon
var timeOutId;

$("#searchIcon").mouseover(function() {
    $("#searchDiv").fadeIn("fast");
    $("#searchIcon").removeClass("disable");

}).mouseleave(function() {
    timeOutId = window.setTimeout(hideInput, 1500);
});

function hideInput(){
    $("#searchDiv").fadeOut(500);
    $("#searchIcon").switchClass("", "disable", 500);
}

// Maneja el filtrado de los usuarios searchInput: id del input de texto
$("#searchInput").keydown(function(e) {
    if ( e.which == 27 ){
        $("#searchInput").blur()
    }

}).keyup(function () {
    filter($(this));

}).focus(function() {
  window.clearTimeout(timeOutId);

}).blur(function() {
    if ( !$(this).val() ){
        $("#searchDiv").fadeOut(500);
        $("#searchIcon").switchClass("", "disable", 500);
    }
});

function filter(element) {
    var value = $(element).val().toLowerCase();
    var $rows = $("#rows").find("tr");

    $rows.hide();
    $rows.filter(function() {
        var that
        if (value == ":activo"){
            return $(this).find("input").is(":checked");
        }
        else if (value == ":inactivo"){
            return !($(this).find("input").is(":checked"));
        }
        else{
            that = $(this).find("td.datos");
        }
        return $(that).text().toLowerCase().indexOf(value) > -1;
    }).show();
}