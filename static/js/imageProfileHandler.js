function replaceImage(url){
    let imgEl = document.getElementById('proimage')
    const new_img = '<img class="rounded-circle article-img avatar" src="' + url + '" alt="" onclick="image_clicked()">'
    imgEl.innerHTML = new_img
}
function image_clicked(){
    const img = document.getElementsByName("img")[0];
    img.click()
}
function upload_image(){
    const img = document.getElementById("profileimginput");
    let formData = new FormData();
    formData.append("profileImage", img.files[0]);
    const csrftoken = getCookie('csrftoken');
    fetch('/profiles/savefile', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        body: formData
    }).then(
        response => response.json()
    ).then(
        function(response){
            const url = response.url
            replaceImage(url)
        }
    ).catch(
        error => window.location.replace("/accounts/login/")
    );
}