document.getElementById("button").addEventListener("click",function(){
    const name = document.getElementById("input_name").value;
    const age = document.getElementById("input_age").value;
    const content = document.getElementById("input_content").value;
    if (name.trim() === "" || age.trim() === "" || content.trim() === "") {
        alert("값을 입력해주세요!");
        return;
    }
    document.getElementById("text_name").innerText = name;
    document.getElementById("text_age").innerText = age;
    document.getElementById("text_content").innerText = content;
}
);