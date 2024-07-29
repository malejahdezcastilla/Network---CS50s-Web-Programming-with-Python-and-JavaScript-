function getTokenValue (){
    return test= document.getElementsByName("csrfmiddlewaretoken")[0].value

}

function saveChanges(id) {
    console.log(id);
    let content = document.getElementById(`post-content-id-${id}`).value;
    let postContent= document.getElementById(`content-${id}`);
    const modalEdit= document.getElementById(`staticBackdrop-${id}`);
    console.log(content)

    fetch (`/edit_post/${id}`, {
        method: "PUT",
        headers: {"Content-type":"application/json", "X-CSRFToken": getTokenValue()},
        body: JSON.stringify({
            content: content,

        })
    })
    .then (response => response.json())
    .then(function() {
        postContent.innerHTML = content;
        let hideModal= bootstrap.Modal.getInstance(modalEdit)
        hideModal.hide()
    })
}


function like (id) {
    console.log(id)
    let num_likes= document.getElementById(`likes_${id}`);

    fetch(`/like/${id}`, {
        method: "POST",
        headers: {
            "Content-type": "application/json",
            "X-CSRFToken": getTokenValue()
        }
    })
    .then (async function (response){
        let message= await response.json();
        console.log(message)
        num_likes.innerHTML = message.num_of_likes;
        document.getElementById(`like_button_${id}`).hidden =true;
        document.getElementById(`unlike_button_${id}`).hidden=false;

    })

}

function unlike (id) {
    console.log(id)
    let num_likes= document.getElementById(`likes_${id}`);
    console.log(num_likes)

    fetch(`/unlike/${id}`, {
        method: "DELETE",
        headers: {
            "Content-type": "application/json",
            "X-CSRFToken": getTokenValue()
        }
    })
    .then (async function (response){
        let message= await response.json();
        console.log(message)
        num_likes.innerHTML = message.num_of_likes
        console.log("222",num_likes)
        document.getElementById(`like_button_${id}`).hidden= false;
        document.getElementById(`unlike_button_${id}`).hidden= true;

    })
}