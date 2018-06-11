jQuery(function($)
{
    $(document).ready(function () {

        $(function(){
            $('#menu_button').click(function(){
                $('.ui.sidebar').sidebar('setting', 'transition', 'overlay').sidebar('toggle');
            });
        });

        $(".menutitle").click(function(){
            var submenu = $(this).next("ul");
            console.log('zzz');

            if( submenu.is(":visible") ){
                tmp = $(this).text().replace(/\-/g,'+');
                $(this).text(tmp)
                submenu.slideUp();
            }else{
                tmp = $(this).text().replace(/\+/g,'-');
                $(this).text(tmp)
                submenu.slideDown();
            }
        });

        //사이드메뉴
        $('.submenutitle').each(function(idx)
        {
            var s = $(this),
            a = s.find('li>a');

            a.bind('focus mouseenter', function(e)
            {
                a.removeClass('active');
                $(this).addClass('active');
            });
        });

    });

});