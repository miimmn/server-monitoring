var dataset;

$(function(){
    // 전체 데이터 가져오기
    $.ajax({
      type: "GET",
      url: "/info/getAllInfo",
      success: function (data) {
        dataset = {...data};
        settingHTML(data);
        settingGraph();
      },
      error: function (xhr, status) {
        alert(" 통신 실패");
      },
    });
});

// 5초 간격으로 업데이트
var timer = setInterval(function() {
  $.ajax({
      type: "GET",
      url: "/info/getInfo",
      success: function (data) {
        updateGraph(data);
      },
      error: function (XMLHttpRequest, textStatus, errorThrown) {
        alert("통신 실패.", textStatus);
        clearInterval(timer);
      },
    });
}, 5000);


// 그래프 초기 세팅
function settingHTML(data) {
  var container = $(".graphList");
  var row;
  var col;
  var graphSet;

  // 한 IP에 대한 그래프 set 
  for ( key of Object.keys(data)) {

    graphSet = $("<div>")
              .attr("class", "graphSet")
              .append($("<h3>").attr("class", "pt-3 fw-bold").append(key));
    
    key = key.replaceAll(".","-");

    row = $("<div>").attr("class", "row");
    col = $("<div>")
              .attr("class", "col-6")
              .attr("id", "cpuChart-"+key);    
    row.append(col);
    col = $("<div>")
              .attr("class", "col-6")
              .attr("id", "memChart-"+ key);
    row.append(col);
    graphSet.append(row);

    row = $("<div>").attr("class", "row");
    col = $("<div>")
              .attr("class", "col-6")
              .attr("id", "diskChart-"+ key);
    row.append(col);
    col = $("<div>")
              .attr("class", "col-6")
              .attr("id", "netChart-"+ key);
    row.append(col);

    container.append(graphSet.append(row).append($("<hr>")));
  }
}

// 초기 세팅용
function settingGraph() {
  for ( [key, value] of Object.entries(dataset)) {
    var key = key.replaceAll(".", "-");
    drawCpuGraph(value['cpuData'], "#cpuChart-"+key);
    drawMemGraph(value['memData'], "#memChart-"+key);
    drawDiskGraph(value['diskData'], "#diskChart-"+key);
    drawNetGraph(value['netData'], "#netChart-"+key);    
  }
}

// 업데이트용 
function updateGraph(data) {

  for ( const key of Object.keys(dataset)) {
    var len =  Object.keys(dataset[key]['cpuData']).length;

    if( len >= 120 ) {
      dataset[key]['cpuData'].shift();
      dataset[key]['memData'].shift();  
      dataset[key]['diskData'].shift();  
      dataset[key]['netData'].shift();  
    }
    dataset[key]['cpuData'].push(data[key]['cpuData'][0]);
    dataset[key]['memData'].push(data[key]['memData'][0]);
    dataset[key]['diskData'].push(data[key]['diskData'][0]);
    dataset[key]['netData'].push(data[key]['netData'][0]);
  }

  // 그리기
  for ( [key, value] of Object.entries(dataset)) {
    var key = key.replaceAll(".", "-");
    console.log(value['cpuData']);

    drawCpuGraph(value['cpuData'], "#cpuChart-"+key);
    drawMemGraph(value['memData'], "#memChart-"+key);
    drawDiskGraph(value['diskData'], "#diskChart-"+key);
    drawNetGraph(value['netData'], "#netChart-"+key);    
  }
}


// cpu 그래프
function drawCpuGraph(data, id) {
  $(id).dxChart({
    palette: ["#EF9A9A"],
    dataSource: {
      store: data,
    },
    // 가로 축
    commonSeriesSettings: {
      argumentField: "origin_time",
    },
    margin: {
      bottom: 20,
    },
    scrollBar: {
      visible: true,
    },
    zoomAndPan: {
      argumentAxis: "both",
    },
    // 가로축 값 설정
    argumentAxis: {
      valueMarginsEnabled: "false",
      discreteAxisDivisionMode: "crossLabels",
      grid: {
        visible: true,
      },
      label: {
        customizeText: function (arg) {
          time = arg.value.replace("T", "\n");
          return time;
        },
      },
    },
    // 세로축 값
    valueAxis: {
        name: "CPU Usage",
        title: {
          text: "CPU Usage",
          font: {
            color: "#000000",
          },
        },
        label: {
          font: {
            color: "#000000",
          },
          format : {
            type : "percent"
          },
        },
        visualRange : {
          startValue: 0,
          endValue: 1,
        }
    },
    // 그래프 그릴 거
    series: [
      {
        valueField: "value",
        name: "CPU Usage",
        type: "area",
      },
    ],
    legend: {
      visible: true,
      horizontalAlignment: "center",
      verticalAlignment: "bottom",
    },
    // 제목
    title: {
      text: "CPU usage",
      font: {
        weight: 1000,
      },
    },
    tooltip: {
      enabled: true,
    },
    background: {
        color: '#ffffff'
    }
  });
}


// 메모리 그래프
function drawMemGraph(data, id) {
  $(id).dxChart({
    palette: ["#EF9A9A"],
    dataSource: {
      store: data,
    },
    // 가로 축
    commonSeriesSettings: {
      argumentField: "origin_time",
    },
    margin: {
      bottom: 20,
    },
    scrollBar: {
      visible: true,
    },
    zoomAndPan: {
      argumentAxis: "both",
    },
    // 가로축 값 설정
    argumentAxis: {
      valueMarginsEnabled: "false",
      discreteAxisDivisionMode: "crossLabels",
      grid: {
        visible: true,
      },
      label: {
        customizeText: function (arg) {
          // 띄어쓰기가 T로 넘어오길래... 줄바꿈으로 치환
          time = arg.value.replace("T", "\n");
          return time;
        },
      },
    },
    // 세로축 값
    valueAxis: {
        name: "Mem usage",
        title: {
          text: "Mem usage",
          font: {
            color: "#000000",
          },
        },
        label: {
          font: {
            color: "#000000",
          },
          format : {
            type : "percent"
          },
        },
        visualRange : {
          startValue: 0,
          endValue: 1,
        }
    },
    // 그래프 그릴 거
    series: [
      {
        valueField: "ram_usage",
        name: "RAM Usage",
        type: "area",
      },
    ],
    legend: {
      visible: true,
      horizontalAlignment: "center",
      verticalAlignment: "bottom",
    },
    // 제목
    title: {
      text: "Memory usage",
      font: {
        weight: 1000,
      },
    },
    tooltip: {
      enabled: true,
    },
    background: {
        color: '#ffffff'
    }
  });
}

// 디스크 그래프
function drawDiskGraph(data, id) {
  $(id).dxChart({
    palette: ["#EF9A9A", "#727272"],
    dataSource: {
      store: data,
    },
    // 가로 축
    commonSeriesSettings: {
      argumentField: "origin_time",
    },
    margin: {
      bottom: 20,
    },
    scrollBar: {
      visible: true,
    },
    zoomAndPan: {
      argumentAxis: "both",
    },
    // 가로축 값 설정
    argumentAxis: {
      valueMarginsEnabled: "false",
      discreteAxisDivisionMode: "crossLabels",
      grid: {
        visible: true,
      },
      label: {
        customizeText: function (arg) {
          // 띄어쓰기가 T로 넘어오길래... 줄바꿈으로 치환
          time = arg.value.replace("T", "\n");
          return time;
        },
      },
    },
    // 세로축 값
    valueAxis: [
      {
        name: "Bytes",
        title: {
          text: "Bytes",
          font: {
            color: "#000000",
          },
        },
        label: {
          font: {
            color: "#000000",
          },
        },
      },
    ],
    // 그래프 그릴 거
    series: [
      {
        // axis: "value",
        valueField: "disk_write",
        name: "disk_write",
        type: "area",
      },
      {
        // axis: "value",
        valueField: "disk_read",
        name: "disk_read",
        type: "area",
      },
    ],
    legend: {
      visible: true,
      horizontalAlignment: "center",
      verticalAlignment: "bottom",
    },
    // 제목
    title: {
      text: "Disk IO",
      font: {
        weight: 1000,
      },
    },
    tooltip: {
      enabled: true,
    },
    background: {
        color: '#ffffff'
    }
  });
}


// 네트워크 트래픽 그래프
function drawNetGraph(data, id) {
  $(id).dxChart({
    palette: ["#EF9A9A", "#727272"],
    dataSource: {
      store: data,
    },
    // 가로 축
    commonSeriesSettings: {
      argumentField: "origin_time",
    },
    margin: {
      bottom: 20,
    },
    scrollBar: {
      visible: true,
    },
    zoomAndPan: {
      argumentAxis: "both",
    },
    // 가로축 값 설정
    argumentAxis: {
      valueMarginsEnabled: "false",
      discreteAxisDivisionMode: "crossLabels",
      grid: {
        visible: true,
      },
      label: {
        customizeText: function (arg) {
          // 띄어쓰기가 T로 넘어오길래... 줄바꿈으로 치환
          time = arg.value.replace("T", "\n");
          return time;
        },
      },
    },

    // 세로축 값
    valueAxis: [
      {
        name: "Bytes",
        title: {
          text: "Bytes",
          font: {
            color: "#000000",
          },
        },
        label: {
          font: {
            color: "#000000",
          },
          
        },
      },
    ],
    // 그래프 그릴 거
    series: [
      {
        valueField: "netin",
        name: "netin",
        type: "area",
      },
      {
        valueField: "netout",
        name: "netout",
        type: "area",
      },
    ],
    legend: {
      visible: true,
      horizontalAlignment: "center",
      verticalAlignment: "bottom",
    },
    // 제목
    title: {
      text: "Network traffic",
      font: {
        weight: 1000,
      },
    },
    tooltip: {
      enabled: true,
    },
    background: {
        color: '#ffffff'
    },
  });
}