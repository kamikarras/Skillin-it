
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

    d3.select(".holder")
    .selectAll("article")
    .data(stuff.counts)
    .enter()
    .append("article")
    .attr("draggable", "true")
    .attr("ondragstart", "drag(event)")
    .attr("id", function(d) {return d; })
    .style("display","inline-block")
    .style("font-size", function(d) { 
        if (d > 50) {return "30px";}
            else { return d -10 + "px";}})
    .style("text-align", "center")
    .style("margin","20px")
    .text("lets try this")
    .style("background-color", "pink")
    .style("border", "5px solid pink")
    .style("height", function(d) {return d * 3 + "px"; })
    .style("border-radius", "50%")
    .style("width", function(d) {return d * 3 + "px"; })
    .data(skills)
    .text(function(d) {return d; })
    .data(data.counts)
    .append("p")
    .style("color", "white")
    .style("padding", "30px")
    .text(function(d) {return d; });
    $('#changeme').html(skills);

}
function allowDrop(evt) {
    evt.preventDefault();
}

function drop(evt){
    evt.preventDefault();
    let data = evt.dataTransfer.getData("text");
    $("drop-here").setAttribute(data);
}

function drag(evt){
    evt.dataTransfer.setData("text", evt.target.getAttribute('id'));
}