document.addEventListener('DOMContentLoaded', function() {
    const teamname = window.location.pathname.split('/')[2];
    get_team(teamname)
    salaryoverview()
})


function salaryoverview(){

    var teamname = document.getElementById('teamname').innerText;
    
    var dictreservesalary = document.getElementById('dictreservesalary').innerText;
    var dictstartersalary = document.getElementById('dictstartersalary').innerText;
    var dicttotalsalary = document.getElementById('dicttotalsalary').innerText;

    var reservesalary = JSON.parse(dictreservesalary);
    var startersalary = JSON.parse(dictstartersalary);
    var totalsalary = JSON.parse(dicttotalsalary);
    

    var keysreserves = [];
    var valuesreserves = [];
    for (key in reservesalary){
        keysreserves.push(reservesalary[key][0])
        valuesreserves.push(reservesalary[key][1])
    }
    var keysstarters = [];
    var valuesstarters = [];
    for (key in startersalary){
        keysstarters.push(startersalary[key][0])
        valuesstarters.push(startersalary[key][1])
    }
    var keystotal = [];
    var valuestotal = [];
    for (key in totalsalary){
        keystotal.push(totalsalary[key][0])
        valuestotal.push(totalsalary[key][1])
    }

    console.log(valuestotal)
    var trace3 = {
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

    var trace1 = {
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
}


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
