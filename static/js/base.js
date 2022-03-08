$(document).ready(function () {
    $("nav .search_box button").click(function(){
        let type= $(this).closest(".search_box").find(".type").val()
        let cate= $(this).closest(".search_box").find(".cate").val()
        let txt= $(this).closest(".search_box").find(".input_text").val()
        if(type=='poster_id' && txt == false) {
            alert("작성자로 검색하시려면 검색어를 입력해주세요")
            return
        }
        let tmp_url = "/search?type="+type+"&cate="+cate+"&txt="+txt
        //alert(tmp_url)
        location.href=tmp_url
    })
});