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
            window.location.href = '/'
        }

    })
}

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
