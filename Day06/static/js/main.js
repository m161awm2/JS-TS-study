function loadPosts() {
    fetch("/api/board")
    .then(res => res.json())
    .then(data => {
        const posts = data;
        let html = "";

        for (let i = 0; i < posts.length; i++) {
            html += `
            <div>
                <h3>${posts[i].title}</h3>
                <p>${posts[i].content}</p>
                <small>${posts[i].nickname}</small>
            </div>
            `;
        }

        document.getElementById("post_list").innerHTML = html;
    })
    .catch(error => {
        console.error(error);
    });
}

loadPosts();

document.getElementById("myForm").addEventListener("submit", function(e) {
    e.preventDefault();

    const nickname = document.getElementById("nickname").value;
    const password = document.getElementById("password").value;
    const title = document.getElementById("title").value;
    const content = document.getElementById("content").value;

    if (nickname.trim() === "" || password.trim() === "" || title.trim() === "" || content.trim() === "") {
        alert("값을 모두 채우세요!");
        document.getElementById("message").innerText = "모든 값을 채워주세요";
        return;
    }

    if (nickname === "admin" && password === "Wadmin") {
        alert("당신은 그럴 권한이 없습니다");
        document.getElementById("message").innerText = "해당 이름은 사용할 수 없습니다";
        return;
    }

    fetch("/api/write", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nickname,
            password,
            title,
            content
        })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        document.getElementById("message").innerText = data.message;

        document.getElementById("title").value = "";
        document.getElementById("content").value = "";

        loadPosts();
    })
    .catch(error => {
        console.error(error);
    });
});