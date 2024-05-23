function updateUserdata() {
    if (document.cookie.indexOf('token=') >= 0) {
        fetch("/userdata")
        .then(async function (response) {
            let responseJson = await response.json();
            document.getElementById("balance").innerText = responseJson["balance"];
            document.getElementById("account-link").href = "/account";
            document.getElementById("account-link").innerText = responseJson["username"];
        })
    } else {
        document.getElementById("balance-div").remove();

        document.getElementById("account-link").href = "/login";
        document.getElementById("account-link").innerText = "Login";
    }
}

updateUserdata()