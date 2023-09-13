if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}  

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

function passwordValidate(){
    password = document.getElementById('password').value;
    errorBox = document.getElementById('errorBox');
    const minLength = 8;
    const hasNumber = /\d/.test(password);
    const hasSpecialCharacter = /[!@#$%^&*]/.test(password);
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);

    if(password.length < minLength){
        errorBox.textContent = "Password must have at least 8 characters long";
    }
    else if(!hasNumber){
        errorBox.textContent = "Password must contain at least one digit";
    }
    else if(!hasSpecialCharacter){
        errorBox.textContent = "Password must contain at least one special character";
    }
    else if(!hasUpperCase){
        errorBox.textContent = "Password must contain at least one uppercase letter";
    }
    else if(!hasLowerCase){
        errorBox.textContent = "Password must contain at least one lowercase letter";
    }
    else{
        errorBox.textContent = "";
        btnSignUp = document.getElementById('btnSignUp');
        btnSignUp.disabled = false;
    }
}