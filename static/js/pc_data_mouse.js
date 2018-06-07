var i = 0;
var mouse_data;
var id;
document.addEventListener('DOMContentLoaded', () => {
    const width = document.body.clientWidth - 50;
    const height = document.documentElement.clientHeight - 50;
    console.log('width:' + width);
    console.log('height:' + height);
    append_button(width, height);
    // var mouse_data = new mouse_data_record();
    mouse_data = new mouse_data_record();
});

function gen_random_num(min, max) {
    return parseInt(Math.random() * (max - min + 1) + min, 10);
}

function gen_random_x_y(width, height) {
    var random_x = gen_random_num(50, width);
    var random_y = gen_random_num(110, height);
    var cor = {"x": random_x, 'y': random_y};
    return cor;
}

function append_button(width, height) {
    var self = this;
    var cor = gen_random_x_y(width, height);
    var x = cor['x'] + 'px';
    var y = cor['y'] + 'px';
    const alertString = `<div id="click_div"><button id="alert" class="btn btn-info">点我</button></div>`;
    // var alertNode = $.parseHTML(alertString);
    var templete = document.createElement('template');
    templete.innerHTML = alertString;
    var alertNode = templete.content.firstChild;
    alertNode.style.position = "absolute";
    alertNode.style.left = x;
    alertNode.style.top = y;
    $('body').append(alertNode);
    console.log(i);
    if (i < 15) {
        document.getElementById('alert').addEventListener('click', getAnotherButton);
    }
    else {
        document.getElementById('alert').addEventListener('click', showFinish);
    }


// $('#alert').bind('click',getAnotherButton);

// var d = document.getElementById('click_div');
// d.style.position = "absolute";
    console.log('x:' + x);
    console.log('y:' + y);
// d.style.left = x;
// d.style.top = y;
}

class mouse_data_record {
    constructor() {
        this.pageCoords = [];
        this.pagexy = [];
        this.time=0;
        this.timestamps = [];
        var self = this;
        setInterval(function () {
            // var pagexy = [];
            self._getMousePosition(self);
            // console.log(self.pagexy);
            if (!(self.pagexy.length === 0)) {
                self.pageCoords.push(self.pagexy);
                self.timestamps.push(self.time);
            }
            // console.log(self.pageCoords)
        }, 10);
    };

    clearTimestamps() {
        this.pageCoords = [];
    }

    _getMousePosition(self) {
        document.onmousemove = function (e) {
            self.pagexy = [e.pageX, e.pageY];
            self.time = e.timeStamp;
            // pageCoords.push( [e.pageX,e.pageY]);
            // console.log(e.pageX + ", " + e.pageY);//get page coordinates and storing in array
        }
    }
}

function getAnotherButton() {
    const width = document.body.clientWidth - 50;
    const height = document.documentElement.clientHeight - 50;
    console.log('width1:' + width);
    console.log('height1:' + height);
    $("#click_div").fadeOut(500);
    id = setTimeout(function () {
        $("#click_div").remove();
    }, 500);
    setTimeout(function () {
        append_button(width, height);
    }, 500);
    i += 1;

}

function showFinish() {

    console.log(mouse_data.pageCoords);
    sendRequest('/server/register_keystroke/', {'mouse_xy': mouse_data.pageCoords,'timestamps':mouse_data.timestamps})
        .then((res) => {
            window.clearInterval(id);
            console.log('res:' + res);
            $("#click_div").fadeOut(500);
            setTimeout(function () {
                $("#click_div").remove();
            }, 500);
            // const finishString = `<div class="center_alert"><h1 style="text-align: center"><p>你已完成所有训练项目</p><p>感谢您的参与!</p></h1></div>`;
            // var alertNode = $.parseHTML(finishString);
            // $('.container-fluid').after(alertNode);
            const moreAnimation = `
<div class="space">
<div class="center_alert"><h1 style="text-align: center"><p>你已完成所有训练项目</p><p>感谢您的参与!</p></h1></div>
  <div class="ship">
    <div class="ship-rotate">
      <div class="pod"></div>
      <div class="fuselage"></div>
    </div>
  </div>
  <div class="ship-shadow"></div>
  <div class="mars">
    <div class="tentacle"></div>
    <div class="flag">
      <div class="small-tentacle"></div>
    </div>
    <div class="planet">
      <div class="surface"></div>
      <div class="crater1"></div>
      <div class="crater2"></div>
      <div class="crater3"></div>
    </div>
  </div>
  <div class="test"></div>
</div>`;
            var moreAnimationNode = $.parseHTML(moreAnimation);
            setTimeout(function () {
                $('.container-fluid').after(moreAnimationNode);
            }, 500)
        })
}

function sendRequest(url, data) {
    return new Promise((resolve) => {
        $.post(
            url,
            JSON.stringify(data),
            (data) => {
                console.log(data);
                resolve(data);
            },
            'text'
        ).fail(function () {
            alert('传输失败，请重新进行鼠标认证部分测试')
        });
    })

}