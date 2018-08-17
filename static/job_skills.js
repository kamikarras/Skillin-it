
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
$('#addit').on('click', test);

function test(evt){
    evt.preventDefault();
    let inputs = {
        "cool" : $('#test').text()
    };
    $.get("/addskill.json", inputs);
    console.log(inputs);
}


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
    .attr("id", function(d) {return d; })
    .style("font-size", "15px")
    .style("text-align", "center")
    .text("lets try this")
    .style("background-color", "pink")
    .style("margin", "20px")
    .style("height", "50px" )
    .style("border-radius", "50px")
    .style("width", function(d) {return d * 3 + "px"; })
    .data(skills)
    .text(function(d) {return d; })
    .append("div")
    .style("width", "50px")
    .style("height", "50px")
    .style("background-color", "black")
    .style("display","inline-block")
    .style("border-radius", "50%")
    .style("margin-right","-70px")
    .on('mouseover', function(d, i) {
    d3.select(this)
    .style("border","3px solid white")
    .style("cursor","pointer")
})
    .on('mouseout', function(d, i) {
    d3.select(this)
    .style("border","0px")
})
    .on('click', function(d, i) {
    d3.select('#test').data(skills).style('background-color', 'pink').text(skills[i]).attr("value", [i]);
})
    .data(data.counts)
    .append("p")
    .style("margin-top","10px")
    .style("display","inline-block")
    .style("color", "white")
    .text(function(d) {return d; })
    .data(skills);


}