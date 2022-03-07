const user_id = 'idtest1'
$(document).ready(function () {
    $(".tab_title li").click(function () {
        var idx = $(this).index();
        $(".tab_title li").removeClass("tab_on");
        $(".tab_title li").eq(idx).addClass("tab_on");
        $(".tab_cont > div").hide();
        $(".tab_cont > div").eq(idx).show();
    })

    mypage_list();
});

function mypage_list() {
    $.ajax({
        type: 'GET',
        url: '/mypage/list?user_id=' + user_id,
        data: {},
        success: function (response) {
            let rows = response['mypage_list']
            for (let i = 0; i < rows.length; i++) {
                let title = rows[i]['title']
                let desc = rows[i]['desc']
                let likes = rows[i]['likes']
                let date = rows[i]['datetime']

                let tmp_html = `
                            <div class="list_rows">
                                <span class="list_title">${title}</span>
                                <span class="list_desc">${desc}</span>
                                <span class="list_likes">💖${likes}</span>
                                <span class="list_date">${date}</span>
                            </div>
                        `

                $('#mypage-list').append(tmp_html)
            }
        }
    })
}

function like_list() {
    $('#like-list').empty()
    $.ajax({
        type: 'GET',
        url: '/mypage/like_list?user_id=' + user_id,
        data: {},
        success: function (response) {
            let rows = response['like_list']
            for (let i = 0; i < rows.length; i++) {
                let title = rows[i]['title']
                let desc = rows[i]['desc']
                let likes = rows[i]['likes']
                let date = rows[i]['datetime']

                let tmp_html = `
                            <div class="list_rows">
                                <span class="list_title">${title}</span>
                                <span class="list_desc">${desc}</span>
                                <span class="list_likes">💖${likes}</span>
                                <span class="list_date">${date}</span>
                            </div>
                        `

                $('#like-list').append(tmp_html)
            }
        }
    })
}