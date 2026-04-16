document.getElementById("loginForm").addEventListener("submit",function(event){
event.preventDefault();
const nickname = document.getElementById("input_name").value;
const password = document.getElementById("input_password").value;

fetch("/api/login", { 
    method: "POST",
    headers:{
        "Content-Type" : "application/json"
    },
    body: JSON.stringify({ // 플라스크 서버로 보낼 데이터를 JSON 문자열로 변환
        nickname,
        password
    })
})
.then(res => res.json()) // 서버에서 응답을 JSON으로 변환
.then(data => { // 서버에서 받은 데이터를 처리
    alert(data.message); // 서버에서 받은 메시지를 알림으로 표시
})
.catch(error => {
    console.error("Error:", error); // 에러가 발생한 경우 콘솔에 출력
});
});