function mypage_list() { // 내가 등록한 운동리스트 불러오기
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
                let post_id = rows[i]['post_id']

                let tmp_html = `
                            <div class="list_rows">
                                <span class="list_title">${title}</span>
                                <span class="list_desc">${desc}</span>
                                <span class="list_likes">💖${likes}</span>
                                <span class="list_date">${date}</span>
                                <span class="list_func">
                                    <button class="btn btn-primary" style="margin-right : 10px;">수정</button>
                                    <button class="btn btn-danger" onclick="del_post(${post_id})">삭제</button>
                                </span>
                            </div>
                            </div>
                        `
                $('#mypage-list').append(tmp_html)
            }
        }
    })
}

function like_list() { //스크랩 리스트 불러오기
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
                let post_id = rows[i]['post_id']

                let tmp_html = `
                            <div class="list_rows">
                                <span class="list_title">${title}</span>
                                <span class="list_desc">${desc}</span>
                                <span class="list_likes">💖${likes}</span>
                                <span class="list_date">${date}</span>
                                <span class="list_func">
                                    <button class="btn btn-primary" style="margin-right : 10px;">수정</button>
                                    <button class="btn btn-danger" onclick="del_like(${post_id},'${user_id}')">삭제</button>
                                </span>
                            </div>
                        `

                $('#like-list').append(tmp_html)
            }
        }
    })
}

function del_post(post_id){ // 등록한 포스트 삭제
    if(window.confirm("한번 삭제하면 되돌릴수 없습니다. 그래도 삭제하시겠습니까?")){
        $.ajax({
            type : 'GET',
            url : '/mypage/del_post?post_id='+post_id,
            data : {},
            success : function(response){
                alert(response['msg'])
                window.location.reload()
            }
        })
    }
}

function del_like(post_id){ // 스크랩 삭제
    if(window.confirm("한번 삭제하면 되돌릴수 없습니다. 그래도 삭제하시겠습니까?")){
        $.ajax({
            type : 'GET',
            url : '/mypage/del_like?post_id='+post_id,
            data : {},
            success : function(response){
                alert(response['msg'])
                window.location.reload()
            }
        })
    }
}