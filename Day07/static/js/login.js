document.getElementById("Form").addEventListener("submit",function(){
    const nickname = document.getElementById("input_nickname").value;
    const password = document.getElementById("input_password").value;
    if(nickname.trim() === "" || password.trim === ""){
        document.getElementById("fail") = "값을 제대로 쓰세요!";
        return;
    }
    fetch('/api/login',{
        method:"POST",
        headers:{
            "Content-Type" : "application/json"
        },
        body: JSON.stringify({
            nickname,
            password
        })
    })
    .then(res=>res.json())
    .then(data=>{
        alert(data.message);
    })
    .catch(error=>{
        console.error(error);
    })
})