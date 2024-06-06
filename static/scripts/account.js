let logoutButton = document.getElementById('logout');

function logout() {
    document.cookie = "token= ; expires = Thu, 01 Jan 1970 00:00:00 GMT";
}

logoutButton.addEventListener('click', logout);