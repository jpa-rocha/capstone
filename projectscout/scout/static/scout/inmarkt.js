document.addEventListener('DOMContentLoaded', function() {
    
    showsalary();
    const div = "ALL";
    salarygoals(div);
    salaryassists(div);
    salarytackles(div);
    
        
})

function showsalary(){
    fetch('/totalsalaryapi')
    .then(response => response.json()) 
    .then(salaries =>{
        var starters = salaries[0];
        var keysstarters = [];
        var valuesstarters = [];
        for (const property in starters) {
            keysstarters.push(property)
            valuesstarters.push(starters[property])
        };

        var reserves = salaries[1];
        var keysreserves = [];
        var valuesreserves = [];
        for (const property in reserves) {
            keysreserves.push(property)
            valuesreserves.push(reserves[property])
        };

        var total = salaries[2];
        var keystotal = [];
        var valuestotal = [];
        for (const property in total) {
            keystotal.push(property)
            valuestotal.push(total[property])
        };

        var tracec = {
            x : keysreserves,
            y : valuesreserves,
            type : 'bar',
            name : 'Reserves'
        };
    
        var traceb = {
            x : keysstarters,
            y : valuesstarters,
            type : 'bar',
            name : 'Starters'
        };
    
        var tracea = {
            x : keystotal,
            y : valuestotal,
            type : 'bar',
            name : 'Total'
        };
    
        var data = [tracec, traceb, tracea];
        var layout = {barmode: 'group',
                      title: {
                      text:'Salary Comparison Top 5 Leagues',
                      font: {
                            family: 'Courier New, monospace',
                            size: 15
                        },
                        height : 600
                }
        }
        
        Plotly.newPlot('salaryoverview', data, layout,{displayModeBar: false,
                                                       responsive: true,
                                                       showlegend: true,
                                                       });
    })
    
}

function salarygoals(div){
    fetch(`/salarygoalsapi/${div}`)
    .then(response => response.json()) 
    .then(salaries =>{
        var data = [];
        var amount = [];
        var goals = [];
        var count = 0;
        salaries.forEach(entry => {
            // list with extra data
            var exgoals = `Expected Goals: ${entry['exgoals']}`;
            amount[count] = entry['yearlysalary'];
            goals[count] = entry['goals'];
            this["trace" + count] = {
                x : [entry['yearlysalary']],
                y : [entry['goals']],
                mode: 'markers',
                type: 'scatter',
                name : entry['name'],
                text : [entry['position'], exgoals],
                marker: { color: 'green',
                          size: 10 }
            };
            data[count] = (this["trace" + count])
            count++;
        })
        var maxsal = Math.max(amount)
        var maxgoals = Math.max(goals)
        var layout = {
            xaxis: {
                range: [ 0, maxsal ]
            },
            yaxis: {
                range: [0, maxgoals]
            },
            title:'Salary and Goals Overview - Top 100',
            font: {
                    family: 'Courier New, monospace',
                    size: 15
            },
            showlegend: false,
            scrollZoom: true, 
            responsive: true,
            height : 600
        };
          
        Plotly.newPlot('salarygoals', data, layout, {displayModeBar: false,
                                                     responsive: true});
    })}

    function salaryassists(div){
        fetch(`/salaryassistsapi/${div}`)
        .then(response => response.json()) 
        .then(salaries =>{
            var data = [];
            var amount = [];
            var assists = [];
            var count = 0;
            salaries.forEach(entry => {
                // list with extra data
                var exassists = `Expected Assists: ${entry['exassists']}`;
                amount[count] = entry['yearlysalary'];
                assists[count] = entry['assists'];
                this["trace" + count] = {
                    x : [entry['yearlysalary']],
                    y : [entry['assists']],
                    mode: 'markers',
                    type: 'scatter',
                    name : entry['name'],
                    text : [entry['position'], exassists],
                    marker: { color: 'blue',
                              size: 10 }
                };
                data[count] = (this["trace" + count])
                count++;
            })
            var maxsal = Math.max(amount)
            var maxassists = Math.max(assists)
            var layout = {
                xaxis: {
                    range: [ 0, maxsal ]
                },
                yaxis: {
                    range: [0, maxassists]
                },
                title:'Salary and Assists Overview - Top 100',
                font: {
                        family: 'Courier New, monospace',
                        size: 15
                },
                showlegend: false,
                scrollZoom: true, 
                height : 600
            };
              
            Plotly.newPlot('salaryassists', data, layout, {displayModeBar: false,
                                                           responsive: true});
        })}

        function salarytackles(div){
            fetch(`/salarytacklesapi/${div}`)
            .then(response => response.json()) 
            .then(salaries =>{
                var data = [];
                var amount = [];
                var tackles = [];
                var count = 0;
                salaries.forEach(entry => {
                    // list with extra data
                    var extackles = `Expected Tackles: ${entry['sucessvsdribble']}`;
                    amount[count] = entry['yearlysalary'];
                    tackles[count] = entry['tackles'];
                    this["trace" + count] = {
                        x : [entry['yearlysalary']],
                        y : [entry['tackles']],
                        mode: 'markers',
                        type: 'scatter',
                        name : entry['name'],
                        text : [entry['position'], extackles],
                        marker: { color: 'orange',
                                  size: 10 }
                    };
                    data[count] = (this["trace" + count])
                    count++;
                })
                var maxsal = Math.max(amount)
                var maxassists = Math.max(tackles)
                var layout = {
                    xaxis: {
                        range: [ 0, maxsal ]
                    },
                    yaxis: {
                        range: [0, maxassists]
                    },
                    title:'Salary and Tackles Overview - Top 100',
                    font: {
                            family: 'Courier New, monospace',
                            size: 15
                    },
                    showlegend: false,
                    scrollZoom: true, 
                    height : 600
                };
                  
                Plotly.newPlot('salarytackles', data, layout, {displayModeBar: false,
                                                               responsive: true});
            })}