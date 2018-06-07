/** Example of client frontend code */

// 添加监听函数，当页面完全加载成功，执行两个bind函数
document.addEventListener('DOMContentLoaded', () => {
    bindRegisterForm();
    // bindAuthForm();
});

// 绑定注册表的事件，
function bindRegisterForm() {
    const loginInput = document.getElementById('id_username'); //账户名
    const passwordInput = document.getElementById('id_password'); //密码
    const formEl = document.getElementById('registerForm'); //整个form
    const keyStokeService = new KeyStrokeAuthService({loginInput, passwordInput}); //添加一个击键监听事件，监听的是输入账户名和密码的input单元
    registerSubmitHandler(formEl, keyStokeService.registerKeystroke, [loginInput, passwordInput]);//提交成功则清除数据，否则显示无信息
}

// function bindAuthForm() {
//     const loginInput = document.getElementById('authLoginInput');
//     const passwordInput = document.getElementById('authPasswordInput');
//     const formEl = document.getElementById('authForm');
//     const keyStokeService = new KeyStrokeAuthService({loginInput, passwordInput});
//     registerSubmitHandler(formEl, keyStokeService.authenticateKeystroke, [loginInput, passwordInput])
// }

function registerSubmitHandler(formEl, submitEndPoint, inputElms) {
    formEl.addEventListener('submit', (e) => {
        e.preventDefault();
        submitEndPoint()
            .then(res => {
                inputElms.forEach(inputEl => inputEl.value = '');
                if (res.message) {
                    // alert('成功');
                    showAlert(formEl, res.message);
                    // setTimeout("invisiable_button()", 1500)
                    invisiable_button();
                }
                console.log(res);
            })
            .catch((err) => {
                showAlert(formEl, 'Error occurred. Please clear fields and/or try again later');
                console.log(err);
            })
    })
}

function showAlert(el, message) {
    $(el).find('.alert').remove();
    const alertNode = getAlert(message);
    $(el).append(alertNode);
    const $alert = $(el).find('.alert');
    // setTimeout(() => $alert.alert('close'), 5000)
}

function getAlert(message) {
//     const alertString = `
// <div class="alert alert-primary alert-dismissible fade show mt-2" role="alert" id="alert">
// 		<span class="alert-message">${message}</span>
// 		<button type="button" class="close" data-dismiss="alert" aria-label="Close">
// 				<span aria-hidden="true">&times;</span>
// 		</button>
// </div>
// `;
    const alertString = `<center id="center"><button id="alert">${message}</button></center>`;
    return $.parseHTML(alertString);
}

function invisiable_button() {
    var but = document.getElementById('center');
    $("#center").fadeOut(3000);
    console.log(but.innerHTML);
    setTimeout(function(){but.remove()},3000);

}