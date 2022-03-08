function post() {
    let title = $('#title').val()
    let desc = $('#desc').val()
    let process = $('#process').val()
    let day1 = $('#day1').val()
    let day2 = $('#day2').val()
    let day3 = $('#day3').val()
    let day4 = $('#day4').val()
    let day5 = $('#day5').val()
    let day6 = $('#day6').val()
    let day7 = $('#day7').val()

    $.ajax({
        type: "POST",
        url: "/health/post",
        data: {
            'title': title,
            'desc': desc,
            'process': process,
            'day1': day1,
            'day2': day2,
            'day3': day3,
            'day4': day4,
            'day5': day5,
            'day6': day6,
            'day7': day7
        },
        success: function (response) {
            alert(response['msg'])
        }

    })
}

function share(post_id) {
    $.ajax({
        type: 'POST',
        url: '/health/share?post_id=' + post_id,
        data: {'post_id': post_id},
        success: function (response) {
            console.log(response)
            window.location.reload()
        }
    })
}

function share_cancel(post_id) {
    $.ajax({
        type: 'POST',
        url: '/health/share_cancel?post_id=' + post_id,
        data: {'post_id': post_id},
        success: function (response) {
            console.log(response)
            window.location.reload()
        }
    })
}

// function del_like(post_id, user_id){ // 스크랩 삭제
//     if(window.confirm("한번 삭제하면 되돌릴수 없습니다. 그래도 삭제하시겠습니까?")){
//         $.ajax({
//             type : 'GET',
//             url : '/mypage/del_like?post_id='+post_id+'&user_id='+user_id,
//             data : {},
//             success : function(response){
//                 alert(response['msg'])
//                 window.location.reload()
//             }
//         })
//     }
// }