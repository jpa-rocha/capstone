document.addEventListener('DOMContentLoaded', function() {
    
    
    document.addEventListener('click', event =>{
        const element = event.target;
        if (element.className.includes("teamnames")){
            url = location.href
            window.location.href = url + `team/${element.id}`    
        }
        else if (element.className.includes("leaguenames")){
            url = location.href
            window.location.href = url + `league/${element.id}`    
        }
    })
        
})