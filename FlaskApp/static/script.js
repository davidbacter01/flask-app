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


function renderPost(postId, username) {
    fetch(`/api/post/${postId}`)
    .then((response) => response.json())
        .then((post) => {
            let container = document.createElement("div");
            container.classList.add("view-post");
            let title = document.createElement("h1");
            title.innerText = post.title;
            container.appendChild(title);
            let details = document.createElement("div");
            details.classList.add("post-info");
            let id = document.createElement("small");
            id.innerText = post.post_id;
            id.id = "id_number";
            let owner = document.createElement("small");
            owner.innerText = `by ${post.owner}`;
            let added = document.createElement("small");
            added.innerText = `Added on: ${post.created_at}`
            let modified = document.createElement("small");
            modified.innerText = `Last modified on: ${post.modified_at}`;
            details.appendChild(id);
            details.appendChild(owner);
            details.appendChild(added);
            details.appendChild(modified);
            container.appendChild(details);
            let image = document.createElement("img");
            image.src = post.image;
            container.appendChild(image);
            let contents = document.createElement("div");
            contents.classList.add("post-content");
            let text = document.createElement("pre");
            text.innerText = post.contents;
            contents.appendChild(text);            
            if (username == post.owner || username == "admin") {
                let editBtn = document.createElement("a");
                editBtn.href = `/edit/${postId}`;
                editBtn.classList.add("button");
                editBtn.innerText="Edit"
                contents.appendChild(editBtn);
                let deleteBtn = document.createElement("a");
                deleteBtn.href = `/delete/${postId}`;
                deleteBtn.classList.add("button");
                deleteBtn.classList.add("red");
                deleteBtn.setAttribute("onclick", "promptUserForDeleteConfirmation()");
                deleteBtn.innerText = "Delete";
                contents.appendChild(deleteBtn);
            }
            container.appendChild(contents);
            document.body.append(container);
    })
}