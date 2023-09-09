function deleteNote(noteId){
    fetch('/delete-note', {
        method: "POST",
        body: JSON.stringify({noteId: noteId}),
    }) .then((_res)=>{
        window.location.href= "/";
    });
}

function shareNote(noteId){
    shareEmail = document.getElementById('shareEmail').value
    fetch('/share-note', {
        method: "POST",
        body: JSON.stringify({noteId, shareEmail}),
    }) .then((_res)=>{
        window.location.href= "/";
    });
}

function setEnabled(){
    firstName = document.getElementById('firstName');
    lastName = document.getElementById('lastName');
    age = document.getElementById('age');
    address = document.getElementById('address');
    btnUpdate = document.getElementById('btnUpdate');

    firstName.disabled = false;
    lastName.disabled = false;
    age.disabled = false;
    address.disabled = false;
    btnUpdate.disabled = false;
}