// let dataset = [1, 2, 3, 4, 5];
"use strict";


d3.json("/data.json", test);

function test(data) {
    let counts = d.counts;
    console.log("hello")
    return console.log(counts);
}



function replaceStuff(results) {
    let status = results;
    $('#changeme').html(status.counts);
    console.log(status.counts);
    console.log("replaced it");
}

function updateStuff() {
    $.get('/data.json', {order: 123}, makeLayout);
    console.log("sent ajax");
}
$('#changeit').on('click', updateStuff);






function makeLayout(data){
    let stuff = data;
    // console.log("hit makeLayout");
    
    // console.log("data" + stuff + "\nStatus" + status);

    d3.select("body")
    .selectAll("article")
    .data(stuff.counts)
    .enter()
    .append("article")
    .text("lets try this")
    .style("background-color", "rgba(100,255,255,0.2")
    .style("margin", "10px")
    .style("position", "absolute")
    .style("right", "0")
    .style("height", "50px")
    .style("top", function(d) {return d * 60+100 + "px"; })
    .style("width", function(d) {return d * 100 + "px"; })
    .text(function(d) {return d; });
    $('#changeme').html(stuff.counts);

}
