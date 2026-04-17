const postList = document.getElementById("post_list");

fetch("/api/board")
    .then(res => res.json())
    .then(posts => {
        postList.innerText = "";
        posts.forEach(post => {
            postList.innerHTML += `
                <article style="margin-bottom:20px;">
                    <h4>
                        <a href="/detail/${post.id}">${post.title}</a>
                    </h4>
                    <p>${post.content}</p>
                    <small>작성자: ${post.nickname}</small>
                </article>
                <hr>
            `;
            });
    })
    .catch(error => {});