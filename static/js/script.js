function toggle_sign_up() {
    $("#btn-check-dup").toggleClass("is-hidden")
    $("#help-id").toggleClass("is-hidden")
    $("#help-password").toggleClass("is-hidden")
    $("#help-password2").toggleClass("is-hidden")
    $("#help-password2").toggleClass("is-hidden")
}

// 간단한 회원가입 함수입니다.
// 아이디, 비밀번호, 닉네임을 받아 DB에 저장합니다.
function signup() {
    $.ajax({
        type: "POST",
        url: "/user/api/signup",
        data: {
            id_give: $('#user_id').val(),
            pw_give: $('#password').val(),
            nickname_give: $('#nick').val(),
            selprgm_give: $('#sel_program').val(),
            scrprgm_give: $('#scr_program').val(),
            mass_give: $('#mass').val(),  //TODO mass, str, funct 체크박스 value 받아와 배열로 만들 것.
            str_give: $('#str').val(),    //TODO mass, str, funct 체크박스 value 받아와 배열로 만들 것.
            funct_give: $('#funct').val() //TODO mass, str, funct 체크박스 value 받아와 배열로 만들 것.
        },
        success: function (response) {
            if (response['result'] == 'success') {
                alert('회원가입이 완료되었습니다.')
                window.location.href = '/user/login'
            } else {
                alert(response['msg'])
            }
        }
    })
}

//(?=.*[a-zA-Z]):해당문자가 반드시 입력될 것.
//[-a-zA-Z0-9_.]:해당문자 사용 사능.
//{2,18}:최소 2자리에서 최대 18자리까지 사용 가능.
function is_nickname(asValue) {
    var regExp = /^(?=.*[a-zA-Z])[-a-zA-Z0-9_.]{2,18}$/;
    return regExp.test(asValue);
}

//(?=.*\d):\d는 숫자를 의미. 반드시 입력될 것.
//(?=.*[a-zA-Z]):알파벳 소문자, 대문자 반드시 입력될 것.
//[0-9a-zA-Z!@#$%^&*]:해당문자 사용 가능.
//{8,20}:최소 8자리에서 최대 20자리 사용 가능.
function is_password(asValue) {
    var regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/;
    return regExp.test(asValue);
}

// ['쿠키'라는 개념에 대해 알아봅시다]
// 로그인을 구현하면, 반드시 쿠키라는 개념을 사용합니다.
// 페이지에 관계없이 브라우저에 임시로 저장되는 정보입니다. 키:밸류 형태(딕셔너리 형태)로 저장됩니다.
// 쿠키가 있기 때문에, 한번 로그인하면 네이버에서 다시 로그인할 필요가 없는 것입니다.
// 브라우저를 닫으면 자동 삭제되게 하거나, 일정 시간이 지나면 삭제되게 할 수 있습니다.
function login() {
    $.ajax({
        type: "POST",
        url: "/user/api/login",
        data: {id_give: $('#user_id').val(), pw_give: $('#password').val()},
        success: function (response) {
            if (response['result'] == 'success') {
                // 로그인이 정상적으로 되면, 토큰을 받아옵니다.
                // 이 토큰을 mytoken이라는 키 값으로 쿠키에 저장합니다.
                $.cookie('mytoken', response['token'], {path: '/'});

                alert('로그인 완료!')
                window.location.href = '/'
            } else {
                // 로그인이 안되면 에러메시지를 띄웁니다.
                alert(response['msg'])
            }
        }
    })
}

function check_dup() {
    let username = $("#user_id").val()
    console.log(username)
    if (username == "") {
        $("#help-id").text("아이디를 입력해주세요.").removeClass("is-safe").addClass("is-danger")
        $("#user_id").focus()
        return;
    }
    if (!is_nickname(username)) {
        $("#help-id").text("아이디의 형식을 확인해주세요. 영문과 숫자, 일부 특수문자(._-) 사용 가능. 2-10자 길이").removeClass("is-safe").addClass("is-danger")
        $("#user_id").focus()
        return;
    }
    $("#help-id").addClass("is-loading")
    $.ajax({
        type: "POST",
        url: "/user/api/signup/check_dup",
        data: {
            username_give: username
        },
        success: function (response) {

            if (response["exists"]) {
                $("#help-id").text("이미 존재하는 아이디입니다.").removeClass("is-safe").addClass("is-danger")
                $("#user_id").focus()
            } else {
                $("#help-id").text("사용할 수 있는 아이디입니다.").removeClass("is-danger").addClass("is-success")
            }
            $("#help-id").removeClass("is-loading")

        }
    });
}