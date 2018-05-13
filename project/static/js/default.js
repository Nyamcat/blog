$(function(){
    $('#menu_button').click(function(){
        $('.ui.sidebar').sidebar('setting', 'transition', 'overlay').sidebar('toggle');
    });
});