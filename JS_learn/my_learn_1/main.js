/**
 * Created by admin on 2018/1/31.
 */

//console.log('main.js loaded');  // 在控制台打印任何内容

//使用jQuery // 将js放在这个函数中，用于保证html在js执行前加载完成
$(document).ready(function () {
    'use strict';  // 让js解释器更严格的对待所写代码
    paper.install(window);  // 将Paper.js注册为一个全局变量
    paper.setup(document.getElementById('mainCanvas'));  // 将Paper.js附在canvas上

    // var c = new Path.Circle(new Point(100, 70), 50);  //画圆
    // c.fillColor = 'green';
    // var rectangle = new Rectangle(new Point(200, 200), new Point(150, 100));
    // var cornerSize = new Size(20, 20);
    // var path = new Path.RoundRectangle(rectangle, cornerSize);
    // path.fillColor = 'black';
    var text = new PointText(200, 200);
    text.justification = 'center';
    text.fontColor = 'white';
    text.fontSize = 20;
    text.content = 'hello world';

    var tool = new Tool();

    tool.onMouseDown = function (event) {  //监听鼠标点击
        var c = new Path.Circle(event.point, 20);  //画圆
        c.fillColor = 'green';
    };

    paper.view.draw();  // 使用Paper.js在屏幕上绘画
//    console.log('main.js loaded');
});