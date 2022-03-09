$(document).ready(function () {
    $("nav .search_box button").click(function () {
        let type = $(this).closest(".search_box").find(".type").val()
        let cate = $(this).closest(".search_box").find(".cate").val()
        let txt = $(this).closest(".search_box").find(".input_text").val()
        if (type == 'poster_id' && txt == false) {
            alert("작성자로 검색하시려면 검색어를 입력해주세요")
            return
        }
        let tmp_url = "./?type=" + type + "&cate=" + cate + "&txt=" + txt
        //alert(tmp_url)
        location.href = tmp_url
    })

    if (isLogin('mytoken')) {
        $('nav .member').removeClass('dn');
        $("nav .guest").removeClass('dn');
        $("nav .guest").addClass('dn');
    } else {
        $("nav .guest").removeClass('dn');
        $("nav .member").removeClass('dn');
        $("nav .member").addClass('dn');
    }

    YesScroll()
});

function isLogin(key) {
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

let oneTime = false; // 일회용 글로벌 변수


function YesScroll() {
    document.addEventListener('scroll', OnScroll, {passive: true}) // 스크롤 이벤트함수정의
    function OnScroll() { //스크롤 이벤트 함수
        let total_cards = $(".card_wrap .card").length; // 페이지네이션 정보획득
        if ($(window).scrollTop() + $(window).height() == $(document).height()) { // 만약 전체높이-화면높이/2가 스크롤포지션보다 작아진다면, 그리고 oneTime 변수가 거짓이라면
            oneTime = true; // oneTime 변수를 true로 변경해주고,
            getData(total_cards, 12); // 컨텐츠를 추가하는 함수를 불러온다.
        }
    }
}

function getData(offset, limit) {
    //console.log('getdata 들어왔따')
    $.ajax({
        type: 'GET',
        url: '/view_list',
        data: {offset: offset, limit: limit},
        success: function (response) {
            let rows = response['post_list']
            for (let i = 0; i < rows.length; i++) {
                let title = rows[i]['title']
                let desc = rows[i]['desc']
                let process = rows[i]['process']
                let likes = rows[i]['likes']
                let date = rows[i]['datetime']
                let poster_id = rows[i]['poster_id']
                let tmp_html = ''
                tmp_html = `<div class="card">
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
            console.log(rows.length + "만큼 붙였다")
            oneTime = false;
        }
    })
}

