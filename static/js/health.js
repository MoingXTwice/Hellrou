// 헬루 등록
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

    // 운동 명, 운동 설명, 운동 프로그램 실행 방법은 반드시 값이 필요하고 설정한 값의 길이를 초과하면 작성할 수 없다.
    if (title == "") {
        alert('운동 명을 입력해주세요.')
        return;
    } else if (title.length > 30) {
        alert('운동 명은 30자까지 입력 가능합니다.')
        return;
    } else if (desc == "") {
        alert('운동 설명을 입력해주세요.')
        return;
    } else if (desc.length > 30) {
        alert('운동 설명은 30자까지 입력 가능합니다.')
        return;
    } else if (process == "") {
        alert('운동 프로그램 실행 방법을 입력해주세요.')
        return;
    }

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
            let post_id = response['post_id']
            alert(response['msg'])
            window.location.href = '/health?post_id=' + post_id
        }

    });
}

// 헬루 수정
function modify(post_id) {
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

    // 운동 명, 운동 설명, 운동 프로그램 실행 방법은 반드시 값이 필요하고 설정한 값의 길이를 초과하면 작성할 수 없다.
    if (title == "") {
        alert('운동 명을 입력해주세요.')
        return;
    } else if (title.length > 30) {
        alert('운동 명은 30자까지 입력 가능합니다.')
        return;
    } else if (desc == "") {
        alert('운동 설명을 입력해주세요.')
        return;
    } else if (desc.length > 30) {
        alert('운동 설명은 30자까지 입력 가능합니다.')
        return;
    } else if (process == "") {
        alert('운동 프로그램 실행 방법을 입력해주세요.')
        return;
    }

    $.ajax({
        type: "POST",
        url: "/health/modify?post_id=" + post_id,
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
            // let post_id = response['post_id']
            alert(response)
            alert(response['msg'])
            window.location.href = '/health?post_id=' + post_id
        }

    });
}

// 공유하기
function share(post_id) {
    $.ajax({
        type: 'POST',
        url: '/health/share?post_id=' + post_id,
        data: {'post_id': post_id},
        success: function (response) {
            window.location.reload()
        }
    })
}

// 공유 취소
function share_cancel(post_id) {
    $.ajax({
        type: 'POST',
        url: '/health/share_cancel?post_id=' + post_id,
        data: {'post_id': post_id},
        success: function (response) {
            window.location.reload()
        }
    })
}

// 스크랩하기
function scrap(post_id) {
    $.ajax({
        type: 'POST',
        url: '/health/scrap?post_id=' + post_id,
        data: {'post_id': post_id},
        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        }
    })
}

// 선택하기
function select(post_id) {
    $.ajax({
        type: 'POST',
        url: '/health/select?post_id=' + post_id,
        data: {'post_id': post_id},
        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        }
    })
}
