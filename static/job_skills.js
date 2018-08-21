
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

function getSkillDetails(evt) {
    evt.preventDefault();
    let input = {
        "skill" : $('#test').text()
    };
}

function makeLayout(data){
    let w = 800,
        h = 500;
    console.log("make layout");
    let stuff = data;
    let skills = stuff.skills;
    let counts = stuff.counts;
    // console.log("hit makeLayout");
    console.log(skills);

    let scaling = d3.scaleLinear()
        .domain([0, 200])
        .range([0,w]);


    let axis = d3.axisBottom()
        .ticks(5)
        .scale(scaling);
    
    let transition =d3.transition();

    let canvas = d3.select(".holder")
        .append("svg")
        .attr("width", w)
        .attr("height", h);

    let group = canvas.append("g");

    let line_d = [0];

    let line = d3.line()
        .x(function(d, i) {return i * 200;})
        .y(function(d, i) {return h - d;})
        .curve(d3.curveCatmullRom.alpha(0.5));


    group.selectAll("path")
        .data([counts])
        .enter()
        .append("path")
        .attr("d", line)
        .attr("fill", "white")
        .attr("stroke", "white")
        .attr("stroke-width", 500)
        .exit();

    group.selectAll("path")
        .append("path")
        .attr("d", function(){
            return 'M 0 400 L 480 0 L 740 200 L 480 400';
        })
        .attr("fill", "black")
        .attr("stroke", "white")
        .attr("stroke-width", 500);

    // let bars = canvas.selectAll("rect")
    //     .data(counts)
    //     .enter()
    //     .append("rect")
    //     .attr("y", function(d,i) {
    //         return i * 60;
    //     })
    //     .attr("height", 50)
    //     .attr("width", 0)
    //     .attr("fill", "white");
    // bars.transition()
    //     .attr("width", function(d){
    //         return scaling(d);
    //     });

    // canvas.append("g")
    //     .attr("transform", "translate(0,400)")
    //     .call(axis);

//     d3.select(".holder")
//     .selectAll("article")
//     .data(stuff.counts)
//     .enter()
//     .append("article")
//     .attr("id", function(d) {return d; })
//     .style("font-size", "15px")
//     .style("text-align", "center")
//     .text("lets try this")
//     .style("background-color", "pink")
//     .style("margin", "20px")
//     .style("height", "50px" )
//     .style("border-radius", "50px")
//     .style("width", function(d) {return d * 3 + "px"; })
//     .data(skills)
//     .text(function(d) {return d; })
//     .append("div")
//     .style("width", "50px")
//     .style("height", "50px")
//     .style("background-color", "black")
//     .style("display","inline-block")
//     .style("border-radius", "50%")
//     .style("margin-right","-70px")
//     .on('mouseover', function(d, i) {
//     d3.select(this)
//     .style("border","3px solid white")
//     .style("cursor","pointer")
// })
//     .on('mouseout', function(d, i) {
//     d3.select(this)
//     .style("border","0px");
// })
//     .on('click', function(d, i) {
//     d3.select('#test').data(skills).style('background-color', 'pink').text(skills[i]).attr("value", skills[i]);
//     d3.select('#test .skill').text(skills[i]);
//     $.get('/skill.json', getSkillDetails);
// })
//     .data(data.counts)
//     .append("p")
//     .style("margin-top","10px")
//     .style("display","inline-block")
//     .style("color", "white")
//     .text(function(d) {return d; })
//     .data(skills);


}