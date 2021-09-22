document.addEventListener('DOMContentLoaded', function() {
    const teamname = window.location.pathname.split('/')[2];
    get_team(teamname);
    salaryoverview(teamname);
})


function salaryoverview(name){
    
    fetch(`/salaryoverviewapi/${name}`)
    .then(response => response.json()) 
    .then(salaries =>{
        var reserves = salaries['reserves'];
        var keysreserves = [];
        var valuesreserves = [];
        reserves.forEach(reserve =>{
            keysreserves.push(reserve[0])
            valuesreserves.push(reserve[1])
        });

        var starters = salaries['starters'];
        var keysstarters = [];
        var valuesstarters = [];
        starters.forEach(starter =>{
            keysstarters.push(starter[0])
            valuesstarters.push(starter[1])
        });

        var total = salaries['total'];
        var keystotal = [];
        var valuestotal = [];
        total.forEach(total =>{
            keystotal.push(total[0])
            valuestotal.push(total[1])
        });

        var trace1 = {
            x : keysreserves,
            y : valuesreserves,
            type : 'bar',
            name : 'Reserves Salaries'
        };
    
        var trace2 = {
            x : keysstarters,
            y : valuesstarters,
            type : 'bar',
            name : 'Starters Salaries'
        };
    
        var trace3 = {
            x : keystotal,
            y : valuestotal,
            type : 'bar',
            name : 'Total Salaries'
        };
    
        var data = [trace1, trace2, trace3];
        var layout = {barmode: 'group'};
    
        Plotly.newPlot('salaryoverview', data, layout,{scrollZoom: true, 
                                                       displayModeBar: false,
                                                       responsive: true,
                                                       showlegend: true,
                                                       });
    })
    

    fetch (`/teamsalaryapi/${name}`)
    .then(response => response.json()) 
    .then(salaries =>{
        startersalarysheet = []
        reservesalarysheet = []
        salaries.forEach(player=>{
            if (player['status'] === 'Starter'){
                entry = []
                entry.push(player['player'])
                entry.push(player['weeklysalary'])
                startersalarysheet.push(entry)   
            }
            else {
                entry = []
                entry.push(player['player'])
                entry.push(player['weeklysalary'])
                reservesalarysheet.push(entry)   
            }
        })
        console.log(startersalarysheet)
        console.log(reservesalarysheet)
        skeys = [];
        svalues = [];
        startersalarysheet.forEach(entry=>{
            skeys.push(entry[0]);
            svalues.push(entry[1]);
        });
            
    
        rkeys = [];
        rvalues = [];
        
        reservesalarysheet.forEach(entry=>{
            rkeys.push(entry[0]);
            rvalues.push(entry[1]);
        });
        
        var traceb = {
            x : skeys,
            y : svalues,
            type : 'bar',
            name : 'Starters Salaries'
        };

        var tracea = {
            x : rkeys,
            y : rvalues,
            type : 'bar',
            name : 'Reserves Salaries'
        };
        var data = [tracea, traceb];
        var layout = {barmode: 'group'};
        Plotly.newPlot('playersalaries', data, layout,{scrollZoom: true, 
                                                    displayModeBar: false,
                                                    responsive: true,
                                                    showlegend: true,
                                                    });
    });      
};


function get_team(name){
    fetch(`/teamapi/${name}`)
    .then(response => response.json())
    .then(statslist =>{
        var playernames = []
        statslist.forEach(stat=>{
            if (stat['name'] != undefined){
           playernames.push(stat['name'])
            }
        });
        
        playernames.forEach(player=>{
            statslist.forEach(stat=>{
                if (stat['name'] == player || stat['player'] == player){
                    var keys = Object.keys(stat)
                    
                    
                }
            });
        });
        
    })
    .catch(error => console.log('error:', error));
}
