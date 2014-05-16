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
        selectionHeader: "<h3>Permisos Actuales</h3>",
        afterInit: function() {
            $("label[for='id_usuarios']").hide()
        }
    });

//    $('.proyecto').multiselectable({
//        selectableLabel: 'Permisos Disponibles',
//        selectedLabel: 'Permisos Elegidos',
//        moveRightText: '',
//        moveLeftText: ''
//    });
//
//    $('.fase').multiselectable({
//        selectableLabel: 'Permisos Disponibles',
//        selectedLabel: 'Permisos Elegidos',
//        moveRightText: '',
//        moveLeftText: ''
//    });
//
//    $('#m-selectable').change( function(){
//        var that = this;
//
//        // Encuentra el elemento seleccionado
//        var valor = $(that).val();
//        var matchedElem = $(that).find('option[value="' + valor + '"]');
//
//        // Obtiene el tipo de permiso
//        var tipo = matchedElem.attr( "data-type" );
//
//        // Segun el tipo de permiso muestra o oculta el select de fases
//        if (tipo == 'fase'){
//            fases.show();
//        }
//        else{
//            fases.hide();
//        }
//
//        //alert(tipo);
//    });
});