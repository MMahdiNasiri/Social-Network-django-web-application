function deletedObj(id, type){
    const obj_id = type + '-' + id
    const btn_id = 'button-' + id
    const obj = document.getElementById(obj_id)
    const btn_obj = document.getElementById(btn_id)
    obj.style.backgroundColor = '#ffd7d7'
    btn_obj.innerHTML = '<button class="btn btn-outline-dark disabled btn-sm ms-3 mt-2">حذف شده</button>'
}

function handleDeleteBtn(id, type) {
    const csrftoken = getCookie('csrftoken');
    const data = {
        'obj_id': id,
        'obj_type': type
    }
    fetch("/controller/delete", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "Content-type": "application/json; charset=UTF-8",
            'X-CSRFToken': csrftoken,
        }
    }).then(response => response.json())
        .then(response => {
            deletedObj(id, type)
        })
}
