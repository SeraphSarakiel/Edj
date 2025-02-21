var mslider = document.getElementById("m-slider");
var moutput = document.getElementById("m-value");
var bslider = document.getElementById("b-slider");
var boutput = document.getElementById("b-value");

var chart = echarts.init(document.getElementById("main"));

moutput.innerHTML = mslider.value;
boutput.innerHTML = bslider.value;

option = {
    xAxis: {
      name: 'x',
      min: -5,
      max: 5
    },
    yAxis: {
      name: 'y',
      min: -5,
      max: 5
    },
    series: [
      {
        data: setData(),
        type: 'line',
      }
    ]
};

chart.setOption(option);



function setData() {
    var result = [];
    for(i=-5;i<=5;i++){
        result.push([i, func(i)]);
    }
    return result;
}

mslider.oninput = function(){
    moutput.innerHTML = this.value;
    chart.setOption({
        series: {
            data:setData()
        }
    });
}

bslider.oninput = function(){
    boutput.innerHTML = this.value;
    chart.setOption({
        series: {
            data:setData()
        }
    });
}

function func(x){
    return Number(mslider.value)*x + Number(bslider.value);
}