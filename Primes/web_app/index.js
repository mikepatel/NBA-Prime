/////////////////////////////////////////////////////////////////////////////////////////////////////
// On load
window.addEventListener("DOMContentLoaded", function(){
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
