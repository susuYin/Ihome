function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}
function logout() {
    $.ajax({
        url: "/api/V1.0/session",
        type: "delete",
        headers: {
            "X-CSRFToken": getCookie("csrf_token")
        },
        dataType: "json",
        success: function (resp) {
            if ("0" == resp.errno) {
                location.href = "/index.html";
            }
        }
    });
}

$(document).ready(function(){
 // 在页面加载是向后端查询用户的信息
    $.get("/api/V1.0/user", function(resp){
        // 用户未登录
        if ("4101" == resp.errno) {
            location.href = "/login.html";
        }
        // 查询到了用户的信息
        else if ("0" == resp.errno) {
            if (resp.data.avatar) {
                $("#user-avatar").attr("src", resp.data.avatar);
            }
            if (resp.data.name) {
                $("#user-name").html(resp.data.name);
            }
            if (resp.data.mobile) {
                $("#user-mobile").html(resp.data.mobile);
            }

        }
    }, "json");
})