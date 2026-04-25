const postList = document.getElementById("post_list");

fetch("/api/board")
    .then(res => res.json())
    .then(posts => { // 응답을 JSON으로 변환
        postList.innerText = ""; // 기존 내용을 초기화
        posts.forEach(post => { // 각 게시글에 대해 HTML을 생성하여 추가
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