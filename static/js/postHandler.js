
function postHeader(username, fullName, profile_img) {
    const img = "<img class='rounded-circle article-img avatar' src='"+ profile_img +"' alt=''>"
    let headName;
    if(fullName){
        headName = "<h5><a href='/profile'" + username + ">" + fullName + "</a></h5>";
    }else{
        headName = '';
    }
    const headUsername = "<em dir='ltr'><a href='/profile'" + username + ">@" + username + "</a></em>";

    const head = img + headName + headUsername;
    return head;
}


function postContent(username, fullName, post_img, content, profile_img){
    const head = postHeader(username, fullName, profile_img)
    let image = ""
    if (post_img){
        image = '<img src="' + post_img + '" alt="" style="width: inherit; max-height: 300px">'
    }
    const lines = content.split(/\r?\n/);
    let lastContent = ''
    lines.forEach(function (value, index, array){
        lastContent += value + '<br>'
    });
    const formattedContent = head + "<div class='ms-2 mt-4'><p></p><p>" + lastContent + "</p></div>" + image
    return formattedContent
}

function postButtons(id) {
    const likeBtn = "<button class='btn btn-primary btn-sm' onclick='handleLikeBtn(" + id
        + ")'> <span class='fa fa-thumbs-up'></span> <span id='postlike-" + id
        + "'> " + 0 + "</span></button>"
    const repubBtn = "<button class='btn btn-primary btn-sm' onclick='handleRepublishBtn("+ id
        + ")'><span class='fa fa-retweet'></span></button>"
    const formattedBtn = "<div class='col-12'><p class='btn-group mt-1'>" + likeBtn + repubBtn + "</p></div>"
    return formattedBtn
}


function carouselFormat(id){
    return "<a href='detail/" + id + "' class='next carousel-control-next fa fa-angle-left' style='font-size:32px; width: 10%;'></a>"
}


function formatPost(id, content, post_img, username, fullName, profile_img){
    const formattedPost = "<div class='col-12 col-md-10 mx-auto border rounded py-3 mb-4 carousel slide post' id='post-" + id
        + "'> "+ postContent(username, fullName, post_img, content, profile_img) + postButtons(id) + carouselFormat(id) + "</div>"
    return formattedPost
}


function formatRepublishElement(id, username, fullName, profile_img, parent){
    const head = postHeader(username, fullName, profile_img)
    const formattedPost = "<div class='col-12 col-md-10 mx-auto border rounded py-3 mb-4 carousel slide post' id='post-" + id
        + "'>" + head + "<div class='col-12 col-md-10 mx-auto border rounded py-3 mb-4 carousel slide post' id='post-"
        + parent.id + "'>" + postContent(parent.username, parent.name, parent.post_img, parent.content, parent.profile_img)
        + carouselFormat(parent.id) + "</div>" + postButtons(id) + carouselFormat(id) + "</div>"
    return formattedPost
}


function handleLikeBtn(id) {
    const csrftoken = getCookie('csrftoken');
    const data = {
        'post_id': id,
    }
    fetch("/like", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "Content-type": "application/json; charset=UTF-8",
            'X-CSRFToken': csrftoken,
        }
    }).then(response => response.json())
        .then(response => document.getElementById("postlike-" + id).innerHTML = response)
        .catch(function(error) {
            window.location.replace("/accounts/login/");
        });
}
function handleRepublishBtn(id){
    const csrftoken = getCookie('csrftoken');
    const data = {
        'post_id': id,
    }
    fetch("/republish", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "Content-type": "application/json; charset=UTF-8",
            'X-CSRFToken': csrftoken,
        }
    }).then(respoonse => respoonse.json())
        .then(response => {
            const id = response.id;
            const parent = response.parent;
            const username = response.username;
            const fullName = response.name;
            const profile_img = response.profile_img;
            const newPostElement = formatRepublishElement(id, username, fullName, profile_img, parent);
            const ogHtml = postsContainerElement.innerHTML;
            postsContainerElement.innerHTML = newPostElement + ogHtml;
        }).catch(response => window.location.replace("/accounts/login/"))
}


const postsContainerElement = document.getElementById("posts")
