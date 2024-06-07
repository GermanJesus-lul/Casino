// logout functionality
function logout() {
    document.cookie = "token= ; expires = Thu, 01 Jan 1970 00:00:00 GMT";
    window.location.href = "/";
}

document.getElementById('logout').addEventListener('click', logout);

// get stats
fetch("/stats")
.then(async function (response) {
    let responseJson = await response.json();

    const stats_div = document.getElementById("stats");
    if (Object.keys(responseJson).length > 0) {
        Object.keys(responseJson).forEach(function (key) {
            const element_div = document.createElement("div");
            element_div.setAttribute("class", "stats-element");

            const header = document.createElement("p");
            header.innerText = key;
            header.setAttribute("class", "stats-element-header");
            element_div.appendChild(header);

            const games_played = document.createElement("p");
            games_played.innerText = responseJson[key]["games_played"];
            games_played.setAttribute("class", "stats-element-entry");
            element_div.appendChild(games_played);

            const balance = document.createElement("p");
            balance.innerText = responseJson[key]["value"];
            balance.setAttribute("class", "stats-element-entry");
            element_div.appendChild(balance);

            stats_div.appendChild(element_div);
        })
    } else {
        const not_played = document.createElement("p");
        not_played.innerText = "No games have been played";
        not_played.setAttribute("class", "stats-element-entry");
        stats_div.appendChild(not_played);
    }
})