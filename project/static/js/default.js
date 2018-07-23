function copyToClipboard(val) {
    var t = document.createElement("textarea");
    document.body.appendChild(t);
    t.value = val;
    t.select();
    document.execCommand('copy');
    document.body.removeChild(t);
}

jQuery(function($)
{
    $(document).ready(function () {

        var submenu = $(".menutitle").next("ul");
        submenu.slideUp();

        $('pre').before('<div class="copy"><button class="copy_button"><p>&nbsp;Copy&nbsp;</p><span class="tooltiptext">Click to Copy</span></button></div>')

        $(document).on('click', '.copy_button', function(){
            $(this).find('.tooltiptext').text('Copied!')
            copyToClipboard($(this).parent().next().find('code').text())
        });

        $(document).on('mouseover', '.copy_button', function(){
                $(this).find('.tooltiptext').text('Click to Copy')
        });

        $(function(){
            $('#menu_button').click(function(e){
                e.stopPropagation();
                $('.ui.sidebar').sidebar('setting', 'transition', 'overlay').sidebar('toggle');
            });
        });

        $("#head").click(function(){
            location.href = '/'
        });

        $(".menutitle").click(function(){
            var submenu = $(this).next("ul");

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