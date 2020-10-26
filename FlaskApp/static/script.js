currentPage = document.getElementById('current');
document.getElementById('prev').value = parseInt(currentPage.innerText) - 1;
document.getElementById('next').value = parseInt(currentPage.innerText) + 1;


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
        link = `/?owner=${username}&page=1`;
    }

    window.location.assign(link);
}

function goToPage(target) {    
    let username = document.getElementById('username').value;
    let link = `/?owner=${username}&page=`;
    if (target == 'next') {
        link += parseInt(currentPage.innerText) + 1;
    } else {
        link += parseInt(currentPage.innerText) - 1;
    }

    window.location.assign(link);
}