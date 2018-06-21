/** `Library` code */
//击键认证服务的主函数
class KeyStrokeAuthService {
    constructor(options) {
        this._loginInput = new KeystrokeInput(options.loginInput); //添加一个账号击键输入事件KeystrokeInput
        this._passwordInput = new KeystrokeInput(options.passwordInput); //添加一个密码击键输入事件KeystrokeInput
        this.registerKeystroke = this.registerKeystroke.bind(this); //post，返回data
        // this.authenticateKeystroke = this.authenticateKeystroke.bind(this); //post成功，返回data
    }

    //post成功则执行清空数据
    registerKeystroke() {
        var username = $('#id_username').val();
        var password = $('#id_password').val();
        // $.ajax({
        //     type: "POST",
        //     async: true,//取消异步 否则flage复制失败
        //     url: "/pc_data/",
        //     datatype: "json",
        //     data: {'username': username, 'password': password},
        //     // 访问完成后执行的方法
        //     success: function (data) {
        //         console.log(data);
        //         if (data === 'false') {
        //             var $jsLoginTips = $('#jsEmailTips');
        //             $jsLoginTips.html("账号或者密码错误，请重新输入").hide();
        //             setTimeout("var $jsLoginTips = $('#jsEmailTips');$jsLoginTips.html(\"账号或者密码错误，请重新输入\").show();", 200);
        //         }
        //
        //         else {
        //             var $jsLoginTips = $('#jsEmailTips');
        //             $jsLoginTips.html("账号或者密码错误，请重新输入").hide();
        //             var intext = document.getElementById('ith-login').innerText;
        //             //console.log('inner:'+intext);
        //             var regex = /(\d{1,2})\//g;
        //             var i = regex.exec(intext)[1];
        //             i = parseInt(i) + 1;
        //             document.getElementById('ith-login').innerText = '第' + i + "/10次登录";
        //             document.getElementById('id_username').value = '';
        //             document.getElementById('id_password').value = '';
        //
        //             if (i === 10) {
        //                 setTimeout("alert('训练完成')", 1000)
        //
        //             }
        //
        //             //console.log(i);
        //         }
        //     }
        // });

        return this._sendRequest('/pc_data_keystroke/', {'username': username, 'password': password})
            .then(res1 => {
                console.log('res1:' + res1);
                this._change_status(res1.toString());
                return res1;
            })
            .then((res2) => {
                    console.log('res2:' + res2);
                    return this._sendRequest('/server/register_keystroke/', {
                        'login': username, 'password': password, "login_timestamps": this._loginInput.timeStamps,
                        "password_timestamps": this._passwordInput.timeStamps,
                    });
                }
            )
            .then(
                res3 => {
                    console.log('res3:' + res3);
                    return res3;
                })

        // .then(res3 => {
        //     this._clearInputsTimestamps();
        //     console.log('res3:' + res3);
        //     return res3;
        // })
        // )


        // return Promise.all([this._sendRequest('/pc_data/', {'username': username, 'password': password})
        //     .then(res1 => {
        //         console.log('res1:' + res1);
        //         this._change_status(res1.toString());
        //         return res1
        //     }),this._sendRequest('/server/register_keystroke/', this._getRequestData())
        //             .then(res3 => {
        //                 this._clearInputsTimestamps();
        //                 console.log('res3:' + res3);
        //                 return res3;
        //             })])

    }


    _change_status(data) {

        // console.log(data);
        if (data === 'false') {
            var $jsLoginTips = $('#jsEmailTips');
            $jsLoginTips.html("账号或者密码错误，请重新输入").hide();
            setTimeout("var $jsLoginTips = $('#jsEmailTips');$jsLoginTips.html(\"账号或者密码错误，请重新输入\").show();", 200);
        }

        else {
            var $jsLoginTips = $('#jsEmailTips');
            $jsLoginTips.html("账号或者密码错误，请重新输入").hide();
            var intext = document.getElementById('ith-login').innerText;
            //console.log('inner:'+intext);
            var regex = /(\d{1,2})\//g;
            var i = regex.exec(intext)[1];
            i = parseInt(i) + 1;
            if (i <= 1) {
                document.getElementById('ith-login').innerText = '第' + i + "/10次登录";
            }
            document.getElementById('id_username').value = '';
            document.getElementById('id_password').value = '';

            if (i === 2) {
                // setTimeout("alert('训练完成')", 1000)
                var form = document.getElementById('registerForm');
                $("#registerForm").fadeOut(1500);
                setTimeout(function () {
                    form.remove()
                }, 1500);

                function add_next_button() {
                    const alertString = `<div class="center_alert"><h1 style="text-align: center">你已完成击键训练，点击下方按钮进入鼠标点击训练</h1><center id="center"><button id="alert" onclick="location='/pc_data_mouse/'">确认进入下一步</button></center></div>`;
                    var alertNode = $.parseHTML(alertString);
                    $("#pc_data_form_div").append(alertNode);
                }

                setTimeout(add_next_button, 1800);


            }

            //console.log(i);
        }

    }

// //post成功则清空数据，返回的是data
// authenticateKeystroke() {
//     return this._sendRequest('/server/authenticate_keystroke/', this._getRequestData())
//         .then(res => {
//             this._clearInputsTimestamps();
//             return res;
//         })
// }

    _clearInputsTimestamps() {
        this._loginInput.clearTimestamps();
        this._passwordInput.clearTimestamps();
    }

    _getRequestData() {
        console.log("login" + this._loginInput.input);
        console.log('password' + this._passwordInput.input);
        return {
            "login": this._loginInput.input.value,
            'password': this._passwordInput.input.value,
            "login_timestamps": this._loginInput.timeStamps,
            "password_timestamps": this._passwordInput.timeStamps,
        }
    }

//发送成功则返回一个promise成功的标志
    _sendRequest(url, data) {
        return new Promise((resolve) => {
            $.post(
                url,
                JSON.stringify(data),
                (data) => resolve(data),
                'json'
            );
        })
    }
}

class KeystrokeInput {
    ///写一个构造函数，用当前的input作为input，用连个array（keydowns，keydownsAndUps）来存放击键的数据
    constructor(input) {
        this.input = input;
        this.timeStamps = {
            keydowns: [],
            keydownsAndUps: [],
        };
        //设置键盘按下和抬起的监听
        this._bindEvents();
    }

    //清空放数据的array
    clearTimestamps() {
        this.timeStamps.keydowns = [];
        this.timeStamps.keydownsAndUps = [];
    }

    //添加对键盘按下去的监听
    _bindEvents() {
        this._bindKeydowns();
        this._bindKeyUps();
    }

    //检测本次按下是否有效，如果无效返回空，有效则把按下去的时间记录下来
    //keydowns只是记录了按下的时间
    //keydownAndUps这个array记录了按下和起来的时间
    _bindKeydowns() {
        this.input.addEventListener('keydown', (e) => {
            if (!this._validateKeyDown(e)) {
                return;
            }
            this.timeStamps.keydowns.push(e.timeStamp);
            this.timeStamps.keydownsAndUps.push(e.timeStamp);
        })
    }

    _bindKeyUps() {
        this.input.addEventListener('keyup', (e) => {
            if (!this._validateKeyDown(e)) {
                return;
            }
            this.timeStamps.keydownsAndUps.push(e.timeStamp);
        })
    }

    _validateKeyDown(e) {
        if (e.code === 'Tab' || e.key === 'Shift' || e.key === 'Enter') {
            return false;
        }
        if (e.code === 'Backspace') {
            this.clearTimestamps();
            this.input.value = '';
            return false;
        }
        if (e.target.value === '') {
            this.clearTimestamps();
        }
        return true;
    }
}

