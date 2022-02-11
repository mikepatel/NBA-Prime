/////////////////////////////////////////////////////////////////////////////////////////////////////
// create a mapping between player names and player plots
let players = new Map();

players.set("Giannis Antetokounmpo", {"src": "images/Giannis Antetokounmpo_plots.png"});
players.set("Kevin Durant", {"src": "images/Kevin Durant_plots.png"});
players.set("LeBron James", {"src": "images/LeBron James_plots.png"});
players.set("Steph Curry", {"src": "images/Stephen Curry_plots.png"});

/////////////////////////////////////////////////////////////////////////////////////////////////////
// On load
window.addEventListener("DOMContentLoaded", function(){
    const dropdown = document.getElementById("dropdown");
    
    // populate dropdown
    for(const [key, value] of players){
        let player_name = key;

        // create a new option element
        let element = document.createElement("option");
        element.textContent = player_name;
        element.value = player_name;

        // add new option element to dropdown
        dropdown.appendChild(element);
    }

    // add listener to dropdown
    dropdown.addEventListener("click", updateImage);
});

/////////////////////////////////////////////////////////////////////////////////////////////////////
// update the image based on the selected option in the dropdown
function updateImage(){
    const playerName = document.getElementById("dropdown").value;
    const player = players.get(playerName);

    if(player !== undefined){
        // find img element and set attributes
        const image = document.querySelector("img");
        image.setAttribute("src", player["src"]);
        image.setAttribute("alt", playerName);
    }    
}

/////////////////////////////////////////////////////////////////////////////////////////////////////
