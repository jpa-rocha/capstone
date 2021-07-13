document.addEventListener('DOMContentLoaded', function() {
    const teamname = window.location.pathname.split('/')[2];
    get_team(teamname)
    salaryoverview()
})


function salaryoverview(){
    var minreservesalary = parseFloat(document.getElementById('minreservesalary').innerText)
    var minstartersalary = parseFloat(document.getElementById('minstartersalary').innerText)
    var mintotalsalary = parseFloat(document.getElementById('mintotalsalary').innerText)

    var percentile25startersalary = parseFloat(document.getElementById('percentile25startersalary').innerText)
    var percentile25reservesalary = parseFloat(document.getElementById('percentile25reservesalary').innerText)
    var percentile25totalsalary = parseFloat(document.getElementById('percentile25totalsalary').innerText)

    var medianreservesalary = parseFloat(document.getElementById('medianreservesalary').innerText)
    var medianstartersalary = parseFloat(document.getElementById('medianstartersalary').innerText)
    var mediantotalsalary = parseFloat(document.getElementById('mediantotalsalary').innerText)

    var percentile75reservesalary = parseFloat(document.getElementById('percentile75reservesalary').innerText)
    var percentile75startersalary = parseFloat(document.getElementById('percentile75startersalary').innerText)
    var percentile75totalsalary = parseFloat(document.getElementById('percentile75totalsalary').innerText)

    var maxreservesalary = parseFloat(document.getElementById('maxreservesalary').innerText)
    var maxstartersalary = parseFloat(document.getElementById('maxstartersalary').innerText)
    var maxtotalsalary = parseFloat(document.getElementById('maxtotalsalary').innerText)

    var teamreservesalary = document.getElementById('teamreservesalary').innerText.replace('€','')
    teamreservesalary = parseFloat(teamreservesalary.replace(',','')) 
    var teamstartersalary = document.getElementById('teamstartersalary').innerText.replace('€','')
    teamstartersalary = parseFloat(teamstartersalary.replace(',',''))
    var totalteamsalary = document.getElementById('totalteamsalary').innerText.replace('€','')
    totalteamsalary = parseFloat(totalteamsalary.replace(',',''))
    
    var trace1 = {
        x: ['Lowest', '25th Percentile', 'Median', '75th percentile', 'Highest'],
        y: [minstartersalary, percentile25startersalary, medianstartersalary, percentile75startersalary, maxstartersalary],
        name: 'Starters Salary',
        type: 'bar'
      };
      
    var trace2 = {
        x: ['Lowest', '25th Percentile', 'Median', '75th percentile', 'Highest'],
        y: [minreservesalary, percentile25reservesalary, medianreservesalary, percentile75reservesalary, maxreservesalary],
        name: 'Reserves Salary',
        type: 'bar'
    };
    
    var trace3 = {
        x: ['Lowest', '25th Percentile', 'Median', '75th percentile', 'Highest'],
        y: [mintotalsalary, percentile25totalsalary, mediantotalsalary, percentile75totalsalary, maxtotalsalary],
        name: 'Total Salary',
        type: 'bar'
    };
    var data = [trace1, trace2, trace3];

    var layout = {title: 'League Salary Distributions',
                  barmode: 'group'};

    Plotly.newPlot('salaryoverview', data, layout,{scrollZoom: true, 
                                                   displayModeBar: false});
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
        })
        playernames.forEach(player=>{
            statslist.forEach(stat=>{
                if (stat['name'] == player || stat['player'] == player){
                    
                }
            })
        })
        
    })
    .catch(error => console.log('error:', error));
}
