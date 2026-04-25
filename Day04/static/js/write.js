document.getElementById("writeForm").addEventListener("submit",function(e){
e.preventDefault();

const title = document.getElementById("input_title").value;
const content = document.getElementById("input_content").value;

fetch("/api/write",{
    method: "POST",
    headers:{
        "Content-Type" : "application/json"
    },
    body: JSON.stringify({
        title,
        content
    })
})
.then(res=>res.json())
.then(data => {
    alert(data.message);
})
.catch(error =>{
    console.error(error);
})
});