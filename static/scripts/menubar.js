function getCookie(name) {
    var cookie = document.cookie;
    var prefix = name + "=";
    var begin = cookie.indexOf("; " + prefix);
    if (begin == -1) {
        begin = cookie.indexOf(prefix);
        if (begin != 0) return null;
    } else {
        begin += 2;
        var end = document.cookie.indexOf(";", begin);
        if (end == -1) {
        end = cookie.length;
        }
    }
    return unescape(cookie.substring(begin + prefix.length, end));
}

function updateUserdata() {
    let token = getCookie("token");
    if (token != null) {
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