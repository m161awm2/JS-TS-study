document.getElementById('signupForm').addEventListener("submit",function(e){
e.preventDefault();
const nickname = document.getElementById("input_name").value;
const password = document.getElementById("input_password").value;

fetch("/api/signup",{
    method: "POST",
    headers:{
        "Content-Type" : "application/json"
    },
    body: JSON.stringify({
        nickname,
        password
    })
})
.then(res => res.json())
.then(data => {
    alert(data.message);
})
.catch(error => {
    console.error(error);
})
});