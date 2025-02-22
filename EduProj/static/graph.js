var chart = echarts.init(document.getElementById("main"));
var graph_daten = JSON.parse(document.getElementById("graph_daten"));
console.log(graph_daten);
console.log(Number(graph_daten[2]));


option = {
    xAxis: {
      name: 'x',
      max: Number(graph_daten[0]),
      min: Number(graph_daten[1])
    },
    yAxis: {
      name: 'y',
      max: Number(graph_daten[2]),
      min: Number(graph_daten[3])
    },
    series: [
      {
        data: setData(),
        type: 'line',
      }
    ]
};

function setData() {
    var result = [];
    for(i=Number(graph_daten[1]); i<=Number(graph_daten[0]); i+=0.1){
        result.push([i, func(i)]);
    }
    return result;
}

function func(x) {
    var result = 0;

    for(i=0; i<=Number(graph_daten[4]); i++){
        result+= Number(graph_daten[4 + i]) * x**Number(graph_daten[4]);
    }
console.log(result);
return result;

}