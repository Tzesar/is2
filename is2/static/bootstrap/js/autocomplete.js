$(document).ready(function() {
    $(window).keydown(function(event){
        if(event.keyCode == 13) {
        event.preventDefault();
        return false;
        }
    });
});



$('#autocomplete').autocomplete({

    serviceUrl: '/userlistjson/LP',
    onSelect: function (suggestion) {
//        console.log('You selected: ' + suggestion.value + ', ' + suggestion.data);
        $('#id_lider_proyecto').val(suggestion.data);
    },
    onHint: function (hint) {
        $('#autocomplete-hint').val(hint);
    }
});
