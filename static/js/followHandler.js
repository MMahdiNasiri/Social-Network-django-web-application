function followBtnHandler(is_following){
    let newBtn = ''
    if (is_following){
        newBtn = '<button class="btn btn-success" onclick="followHandler(false)" >دنبال کردن</button>'
    }else{
        newBtn = '<button class="btn btn-outline-secondary" onclick="followHandler(true)" >توقف پیروی</button>'
    }
    document.getElementById('followBtn').innerHTML = newBtn
}

function followersHandler(is_following){
    let count_followers = document.getElementById('followers').innerText;
    const patt = /\d+/g;
    count_followers = count_followers.match(patt);
    count_followers = parseInt(count_followers);

    if (is_following){
        count_followers -= 1;
    }else{
        count_followers += 1;
    }
    const result = count_followers + ' دنبال کننده '
    document.getElementById('followers').innerText = result

}

function followHandler(is_following){
    const csrftoken = getCookie('csrftoken');
    username = document.getElementById('username').innerHTML
    const data = {
        'followed': is_following,
        'username': username
    }
    fetch("/profiles/follow", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "Content-type": "application/json; charset=UTF-8",
            'X-CSRFToken': csrftoken,
        }
    }).then(response => response.json())
        .then(response => followBtnHandler(is_following, username))
        .then(response => followersHandler(is_following))
        .catch(error => window.location.replace("/accounts/login/"))
}