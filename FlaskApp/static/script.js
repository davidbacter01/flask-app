function promptUserForDeleteConfirmation() {
    if (confirm("Are you sure you want to delete this post?")) {
        document.getElementById("delete").setAttribute("href", "/delete/" + document.getElementById("id_number").innerText)
    } else {
        document.getElementById("delete").setAttribute("href","#")
    }
}