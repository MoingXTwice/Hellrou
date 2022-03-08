$(document).ready(function () {
    $("nav .search_box button").click(function(){
        let type= $(this).closest(".search_box").find(".type").val()
        let cate= $(this).closest(".search_box").find(".cate").val()
        let txt= $(this).closest(".search_box").find(".input_text").val()
        if(type=='poster_id' && txt == false) {
            alert("작성자로 검색하시려면 검색어를 입력해주세요")
            return
        }
        let tmp_url = "search?type="+type+"&cate="+cate+"&txt="+txt
        alert(tmp_url)
        location.href=tmp_url
        //go("search?type="+type+"&cate="+cate+"&txt="+txt)

        /*
        $.ajax({
            type: 'GET',
            url: tmp_url,
            data: {},
            success: function (response) {
                console.log(response)
                let rows = response['post_list']
                if(rows == 0){
                    alert("검색 결과가 없습니다")
                    return
                }


                $('body .inner .card_wrap').empty();
                let a = `
                <div class="inner">
                    <div class="card_wrap" id="card_wrap">
                    </div>
                </div>`
                $('#contents').append(a)
                for (let i = 0; i < rows.length; i++) {
                    let title = rows[i]['title']
                    let desc = rows[i]['desc']
                    let process = rows[i]['process']
                    let likes = rows[i]['likes']
                    let date = rows[i]['datetime']
                    let poster_id = rows[i]['poster_id']
                    let tmp_html=`<div class="card">
                                        <div class="title">${title}</div>
                                        <div class="desc">${desc}</div>
                                        <div class="process">${process}</div>
                                        <div class="date">${date}</div>
                                        <div class="likes">💖${likes}</div>
                                        <div class="poster_id">${poster_id}</div>
                                    </div>
                            `
                    $('#card_wrap').append(tmp_html)
                }

            }
        })
        //alert(tmp_url);
        */

    })
});