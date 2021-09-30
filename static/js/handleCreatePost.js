function handleCreatePost(event){
    event.preventDefault()
    const csrftoken = getCookie('csrftoken');
    const myForm = event.target
    const formData = new FormData();
    const fileField = document.querySelector('input[type="file"]');
    const content = document.getElementById('id_content').value
    formData.append('content', content);
    formData.append('image', fileField.files[0]);


    fetch("/createpost", {
        method: "POST",
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken,
        }
        }).then(response => response.json())
                .then(response =>{
                    const id = response.id
                    const rescontent = response.content
                    const post_img = response.post_img
                    const username = response.username
                    const fullName = response.name
                    const profile_img = response.profile_img
                    const newPostElement = formatPost(id, rescontent, post_img,username, fullName, profile_img)
                    const ogHtml = postsContainerElement.innerHTML
                    postsContainerElement.innerHTML = newPostElement + ogHtml
                    myForm.reset()
                    removeUpload()
                }).catch(function(error) {
                    window.location.replace("/accounts/login/");
                });
    }
const postCreateFormEl = document.getElementById("post-create-form");
postCreateFormEl.addEventListener("submit", handleCreatePost);
