fetch("/api/detail/" + postId)
.then(res => res.json())
.then(data => {
    const post = data.post;
    const comments = data.comments;

    document.getElementById("post_title").innerText = post.title;
    document.getElementById("post_nickname").innerText = post.nickname;
    document.getElementById("post_content").innerText = post.content;

    let html = "";

    for (let i = 0; i < comments.length; i++) {
        html += `<p>${comments[i].nickname} : ${comments[i].content}</p>`;
    }

    document.getElementById("comment_box").innerHTML = html;
})
.catch(error => {
    console.error("Error:", error);
});