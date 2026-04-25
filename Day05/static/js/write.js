document.getElementById("writeForm").addEventListener("submit",function(e){
e.preventDefault();
const nickname = document.getElementById("input_name").value;
const title = document.getElementById("input_title").value;
const content = document.getElementById("input_content").value;
const password = document.getElementById("input_password").value;

if(nickname.trim() === "" || title.trim() === ""|| content.trim() === "" || password.trim() === ""){
document.getElementById("message").innerText = "값을 넣으세요!";
return;
}
else if(password.length < 4){
document.getElementById("message").innerText = "비밀번호는 4글자 이상 작성해주세요!";
return;
}
else if(name === "admin" && password != "Wadmin"){
document.getElementById("message").innerText = "해당 닉네임은 사용 할 수 없습니다";
return;
}
fetch("/api/write",{
    method: "POST",
    headers:{
        "Content-Type" : "application/json"
    },
    body: JSON.stringify({
        nickname,
        title,
        content,
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
})