$('.up_down').on('click', function () {

    // alert(article_id);
    if ('{{request.user.username}}') {
        alert('{{ article_obj.pk }}');
        var obj = $(this);
        var is_up = obj.hasClass('diggit');
        $.ajax({
            url: '/up_down/',
            type: 'post',
            data: {'article_id': '{{ article_obj.pk }}', 'is_up':is_up, 'csrfmiddlewaretoken': $("[name='csrfmiddlewaretoken']").val()},
            success: function (data) {
                if (data.status){
                    if ('{{request.user}}' === '{{ article_obj.author }}') {
                        $('.diggword').text('不能给对自己操作')
                    }else{
                        var num = obj.text();
                        obj.text(parseInt(num)+1)
                    }
                }else{
                    var msg = is_up?'您已推荐过':'你已反对过';
                    $('.diggword').text(msg)
                    }
            }
        })
    }else{
        $('.diggword').text('请先登录')
    }
});