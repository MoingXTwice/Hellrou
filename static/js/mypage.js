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