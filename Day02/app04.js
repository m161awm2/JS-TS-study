document.getElementById("button").addEventListener("click",function(){
    const name = document.getElementById("input_name").value;
    const age = document.getElementById("input_age").value;
    if (name.trim() === "" || age.trim() === ""){
        document.getElementById("text_name").innerText = "값을 넣으세요!"
        document.getElementById("text_age").innerText = "값을 넣으세요!"
    }
    else{
    document.getElementById("text_name").innerText = name
    document.getElementById("text_age").innerText = age
    }
}
);
