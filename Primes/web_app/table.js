/////////////////////////////////////////////////////////////////////////////////////////////////////
// On load
window.addEventListener("DOMContentLoaded", function(){
    // add listener to dropdown
    dropdown.addEventListener("click", updateTable);
});


/////////////////////////////////////////////////////////////////////////////////////////////////////
function updateTable (){
    const playerName = document.getElementById("dropdown").value;
    const player = players.get(playerName);

    if(player !== undefined){
        console.log(playerName);
    }
}
