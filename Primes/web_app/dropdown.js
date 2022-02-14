/////////////////////////////////////////////////////////////////////////////////////////////////////
// create a mapping between player names and player plots
let players = new Map();


/////////////////////////////////////////////////////////////////////////////////////////////////////
// On load
window.addEventListener("DOMContentLoaded", function(){
    // populate 'players' map
    players.set("Giannis Antetokounmpo", {"src": "images/Giannis Antetokounmpo_plots.png"});
    players.set("Kevin Durant", {"src": "images/Kevin Durant_plots.png"});
    players.set("LeBron James", {"src": "images/LeBron James_plots.png"});
    players.set("Steph Curry", {"src": "images/Stephen Curry_plots.png"});

    // get reference to 'dropdown' element
    const dropdown = document.getElementById("dropdown");
    
    // populate dropdown
    for(const [key, value] of players){
        const player_name = key;

        // create a new option element
        const element = document.createElement("option");
        element.textContent = player_name;
        element.value = player_name;

        // add new option element to dropdown
        dropdown.appendChild(element);
    }
});


/////////////////////////////////////////////////////////////////////////////////////////////////////
