
"use strict";

function replaceStuff(results) {
    let status = result.skills;
    console.log(status);
}

function updateStuff(evt) {
    evt.preventDefault();
    let formInputs = {
        "title": $("#title").val(),
        "list_total": $("#list_total").val(),
    };
    $.get('/job_skills.json', formInputs, makeLayout);
    console.log("sent ajax");
}
$('#changeit').on('submit', updateStuff);





function makeLayout(data){
    console.log("make layout")
    let stuff = data;
    let skills = stuff.skills;
    let counts = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
    // console.log("hit makeLayout");
    console.log(skills)
    
    // console.log("data" + stuff + "\nStatus" + status);

    d3.select("body")
    .selectAll("article")
    .data(stuff.counts)
    .enter()
    .append("article")
    .style("font-size", "40px")
    .style("text-align", "center")
    .text("lets try this")
    .style("background-color", "rgba(100,255,255,0.4")
    .style("border", "5px solid pink")
    .style("margin", "10px")
    .style("position", "absolute")
    .style("height", function(d) {return d * 100 + "px"; })
    .style("border-radius", "50%")
    .style("width", function(d) {return d * 100 + "px"; })
    .data(counts)
    .style("right", function(d) {return Math.floor(d * Math.random()) * 80 + "px";})
    .style("top", function(d) {return d * 60 + "px"; })
    .data(skills)
    .text(function(d) {return d; })
    .data(data.counts)
    .append("p")
    .style("color", "white")
    .style("padding", "30px")
    .text(function(d) {return d; });
    $('#changeme').html(skills);

}