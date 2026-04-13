document.getElementById("form01").addEventListener("submit",function(event){
    event.preventDefault();
    const name = document.getElementById("input_name").value;
    const age = document.getElementById("input_age").value;
    const email = document.getElementById("input_email").value;
    if(name.trim() === "" || age.trim() === "" || email.trim() === ""){
        alert("유효한 값을 넣으세요");
    }
    if(isNaN(age)||age<=0){
        alert("제대로된 나이를 쓰세요!");
    }
    document.getElementById("text_name").innerText = name;
    document.getElementById("text_age").innerText = age;
    document.getElementById("text_email").innerText = email;
    
});