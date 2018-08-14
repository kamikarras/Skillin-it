let dataset = [1, 2, 3, 4, 5];

// d3.json('/data.json', makeLayout);
var data = $.get("/data.json");
makeLayout(data);

function makeLayout(data){
    console.log("hit makeLayout");
    console.log(data.keys);
    console.log("data" + data + "\nStatus" + status);

  let practice = d3.select("body")
    .selectAll("article")
    .data(data)
    .enter()
    .append("article")
    .style("background-color", "rgba(100,255,255,0.5")
    .style("margin", "10px")
    .style("position", "absolute")
    .style("right", "0")
    .style("height", "50px")
    .style("top", function(d) {return d * 60+100 + "px"; })
    .style("width", function(d) {return d * 100 + "px"; })
    .text(function(d) {return d; });

}
