$(document).ready(function () {
    get_all_post();
});

function get_all_post(){
    $.ajax({
        type: 'GET',
        url: '/all_list' ,
        data: {},
        success: function (response) {
            console.log(response)
            let rows = response['all_post']

            for (let i = 0; i < rows.length; i++) {
                let title = rows[i]['title']
                let desc = rows[i]['desc']
                let process = rows[i]['process']
                let likes = rows[i]['likes']
                let date = rows[i]['datetime']
                let poster_id = rows[i]['poster_id']
                let tmp_html=''
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
        }
    })
}
function isLogin(){

}
function go(href){

}
