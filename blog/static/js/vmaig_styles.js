/**
 * Created by boyce on 16/8/2.
 */

/* Login -- JS */
$("#logout").click(function () {
    $.ajax({
        type: "POST",
        url: "/vauth/logout",
        beforeSend:function(xhr){
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        },
        success:function(){
            location.replace("/");
        },
        error:function(XMLHttpRequest){
            alert(XMLHttpRequest.responseText);
        }
    })
});

$('#login-form').submit(function () {
    $.ajax({
        type: "POST",
        url: "/vauth/login",
        data:{"username":$("#login-username").val(),"password":$("#login-password").val()},
        beforeSend:function(xhr){
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        },
        success: function (data) {
            var errors = data["errors"];
            if (errors.length==0) {
                location.reload();
            }else{
                var html = "<div class=\"alert alert-danger\">";
                for(var key in errors){
                    html += errors[key]+"<br/>";
                }
                html += "</div>";
                $("#login-modal .modal-header").after(html);
            }
        },
        error:function(XMLHttpRequest){
            alert(XMLHttpRequest.responseText);
        }
    });
    return false;
});

/*Register---js*/

$("#register-form").submit(function () {
    $.ajax({
        type: "POST",
        url: "/vauth/register",
        data:{"username":$("#register-username").val(),"email":$("#register-email").val(),
            "password1":$("#register-password-1").val(),"password2":$("#register-password-2").val()},
        dataType:'json',
        beforeSend:function(xhr){
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        },
        success: function (data) {
            var errors = data["errors"];
            if (errors.length==0) {
                location.reload();
            }else{
                var html = "<div class=\"alert alert-danger\">";
                for(var key in errors){
                    html += errors[key]+"<br/>";
                }
                html += "</div>";
                $("#login-modal .modal-header").after(html);
            }
        },
        error:function(XMLHttpRequest){
            alert(XMLHttpRequest.responseText);
        }
    });
    return false;
});

$("#register-button").click(function(){
    $("#register-modal .alert").remove();
});

/*Widgest Panel js*/
$(function(){
    $('.panel-close').click(function(){
        $(this).parent().parent().parent().hide(300);
    });

    $('.collapse').on('hide.bs.collapse',function(){
        $(this).prev().find(".panel-collapse").removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
    });

    $('.collapse').on('show.bs.collapse',function(){
        $(this).prev().find(".panel-collapse").removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
    });


});

/*_all_posts js*/
$("input[name='category']").click(function () {
    var start = 0;
    var end = 5;

    $("input[name='category']").parent().removeClass("active");
    $("#all-post-more")[0].style.display = "none";
    $("#loading")[0].style.display = "block";

    $("#all-post-list").empty();
    $(this).parent().addClass("active");
    $("#all-post-more").val($(this).val());

    $.ajax({
        type:"POST",
        url:"/all/",
        data:{"val":$(this).attr("value"),"sort":$("input[name='sort']:checked").val(),"start":start,"end":end},
        beforeSend:function(xhr){
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        },
        success:function(data){
            $("#loading")[0].style.display = "none";
            $('#all-post-list').append(data["html"]);
            if(data["isend"])
            {
                $("#all-post-more")[0].style.display = "none";
            }else{
                $("#all-post-more")[0].style.display = "block";
            }
        },
        error:function(XMLHttpRequest){
            alert(XMLHttpRequest.responseText);
        }
    });
});

$("input[name='sort']").click(function () {
    var start = 0;
    var end = 5;
    $("#all-post-more")[0].style.display = "none";
    $("#loading")[0].style.display = "block";

    $("#all-post-list").empty();
    $.ajax({
        type:"POST",
        url:"/all/",
        data:{"val":$("label.active input").val(),"sort":$("input[name='sort']:checked").val(),"start":start,"end":end},
        beforeSend:function(xhr){
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        },
        success:function(data){
            $("#loading")[0].style.display = "none";
            $('#all-post-list').append(data["html"]);
            if(data["isend"])
            {
                $("#all-post-more")[0].style.display = "none";
            }else{
                $("#all-post-more")[0].style.display = "block";
            }
        },
        error:function(XMLHttpRequest){
            alert(XMLHttpRequest.responseText);
        }
    });
});

$("#all-post-more").click(function () {
    var end = 5;
    var start = end;
    end += 5;
    $("#loading")[0].style.display = "block";
    $.ajax({
        type:"POST",
        url:"/all/",
        data:{"val":$(this).attr("value"),"sort":$("input[name='sort']:checked").val(),"start":start,"end":end},
        beforeSend:function(xhr){
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        },
        success:function(data){
            $("#loading")[0].style.display = "none";
            $("#all-post-more")[0].style.display = "none";
            $('#all-post-list').append(data["html"]);

            if(data["isend"])
            {
                $("#all-post-more")[0].style.display = "none";
            }else{
                $("#all-post-more")[0].style.display = "block";
            }
        },
        error:function(XMLHttpRequest){
            alert(XMLHttpRequest.responseText);
        }
    });
});
