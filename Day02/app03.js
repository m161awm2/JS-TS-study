document.getElementById("button").addEventListener("click",function(){
    const content = document.getElementById("input").value;
    document.getElementById("text").innerText = content;
});