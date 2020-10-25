function promptUserForDeleteConfirmation() {
    if (confirm("Are you sure you want to delete this post?")) {
        document.getElementById("delete").setAttribute("href", "/delete/" + document.getElementById("id_number").innerText)
    } else {
        document.getElementById("delete").setAttribute("href","#")
    }
}

function applyFilter() {
    let username = document.getElementById('username').value;
    let link = '';
    if (username == 'All') {
        link = '/';
    }
    else {
        link = `/?owner=${username}`;
    }

    window.location.assign(link);
}