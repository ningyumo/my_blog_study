String.prototype.format = function(){
    var str = this;
    for (var i = 0; i < arguments.length; i++) {
        var str = str.replace(new RegExp('\\{' + i + '\\}', 'g'), arguments[i])
    };
    return str;
};
$("#comment_form").submit(function(){
    //判断是否为空
    $("#comment_error").text("");
    if(CKEDITOR.instances['id_text'].document.getBody().getText().trim()==''){
        $("#comment_error").text("评论内容不能为空");
        return false;

    };
    //更新数据到textarea
    CKEDITOR.instances['id_text'].updateElement();
    //异步提交
    $.ajax({
        url: "/comment/submit/",
        type: "POST",
        data: $(this).serialize(),
        cache: false,
        success: function(data){
            if(data['status']=='SUCCESS'){
                $("#no_comment").remove();
                //插入数据
                if($('#reply_comment_id').val()== 0){
                    var comment_html = "<div id='top_parent_{0}' class='comment'>" + 
                                        "<span>{1}&nbsp; {2}:</span><br><div id='comment_{0}'>" +
                                        "{3}</div><p><a href='javascript:reply({0});'>回复&nbsp;&nbsp;</a>" +
                                        "&nbsp;&nbsp;<span class='like_num' onclick='likechange(this, content_type=\"{4}\", object_id={0})'>" +
                                        "<span class='like glyphicon glyphicon-thumbs-up'></span>" +
                                        "<span class='total_num'>&nbsp;0&nbsp;</span><span>喜欢</span></span></p></div>";                        
                    comment_html = comment_html.format(data['pk'],data['username'], data['comment_time'], data['text'], data['content_type'])

                    $("#comment_list").prepend(comment_html);
                }else{
                    //插入二级评论
                    var reply_html = "<div class='reply'><span>{0}&nbsp;回复&nbsp;" +
                                    "{1}&nbsp;{2}:</span><br><div id='comment_{3}'>" +
                                    "{4}</div><p><a href='javascript:reply({3})''>回复&nbsp;&nbsp;</a>" +
                                    "&nbsp;&nbsp;<span class='like_num' onclick='likechange(this, content_type=\"{5}\", object_id={3})'>" +
                                    "<span class='like glyphicon glyphicon-thumbs-up'></span>" +
                                    "<span class='total_num'>&nbsp;0&nbsp;</span><span>喜欢</span></span></p></div>";
                    reply_html = reply_html.format(data['username'], data['reply_to'], data['comment_time'], data['pk'], data['text'], data['content_type']);
                    $("#top_parent_" + data["top_parent_pk"]).append(reply_html);
                }
                $('#reply_comment_container').hide();
                $('#reply_comment_id').val(0);
                $("#comment_error").text('评论成功')
                //清空编辑框的内容
                CKEDITOR.instances['id_text'].setData('');
            }else{
                //显示错误信息
                $("#comment_error").text(data['message'])
            }
            
        },
        error: function(xhr){
            console.log(xhr);
        },
    });
    return false;
});