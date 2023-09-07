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