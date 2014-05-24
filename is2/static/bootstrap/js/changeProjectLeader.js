$(document).ready(function() {
    $('#id_miembros').multiSelect({
        keepOrder: true,
        selectableHeader: "<h3>Usuarios Disponibles</h3>",
        selectionHeader: "<h3>Miembros Actuales</h3>"
    });

    var miembrosElegidos = $('.ms-selectable .ms-list li').filter(function(){ return $(this).css('display') == 'none'; });
    if (miembrosElegidos.length == 2){
        $('.ms-selectable .ms-list').children().addClass('disabled');
    }
    console.log(miembrosElegidos.length);
});

$('#id_miembros').multiSelect({
    afterSelect: function(){
        var miembrosElegidos = $('.ms-selectable .ms-list li').filter(function(){ return $(this).css('display') == 'none'; });
        if (miembrosElegidos.length == 2){
            $('.ms-selectable .ms-list').children().addClass('disabled');
        }
        console.log(miembrosElegidos.length);
    },
    afterDeselect: function(){
        var miembrosElegidos = $('.ms-selectable .ms-list li').filter(function(){ return $(this).css('display') == 'none'; });
        if (miembrosElegidos.length < 2){
            $('.ms-selectable .ms-list').children().removeClass('disabled');
        }
        console.log(miembrosElegidos.length);
    }
});