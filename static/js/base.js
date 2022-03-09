$(document).ready(function () {
    $("nav .search_box button").click(function(){
        let type= $(this).closest(".search_box").find(".type").val()
        let cate= $(this).closest(".search_box").find(".cate").val()
        let txt= $(this).closest(".search_box").find(".input_text").val()
        if(type=='poster_id' && txt == false) {
            alert("작성자로 검색하시려면 검색어를 입력해주세요")
            return
        }
        let tmp_url = "./?type="+type+"&cate="+cate+"&txt="+txt
        //alert(tmp_url)
        location.href=tmp_url
    })

    if(isLogin('mytoken')){
        $('nav .member').removeClass('dn');
        $("nav .guest").removeClass('dn');
        $("nav .guest").addClass('dn');
    }else{
        $("nav .guest").removeClass('dn');
        $("nav .member").removeClass('dn');
        $("nav .member").addClass('dn');
    }
});

function isLogin(key){
    let result = null;
    let cookie = document.cookie.split(';');
    cookie.some(function (item) {
        // 공백을 제거
        item = item.replace(' ', '');

        var dic = item.split('=');

        if (key === dic[0]) {
            result = dic[1];
            return true;    // break;
        }
    });

    return result;
}