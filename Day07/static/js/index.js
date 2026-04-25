function loadPost(){
fetch('/api/board') // @@@@@@@@@@@@@@@@@@@@@@ 플라스크 안에있는 /api/board 안에 jsonify로 받아온 data를 사용
.then(res=>res.json())
.then(data=>{ // 포스트를 json화한게 data 안에 들어있음
    const posts = data; // posts 변수안에는 닉네임이나 그런게 들어있다!!! @@@@@@@@@@@@@@@@
    let html = "";``
    for(let i = 0; i<posts.length; i++){
        html += `<h2><a href="/detail/${posts[i].id}">${posts[i].title}</a></h2>
        <small>글쓴이: <span>${posts[i].nickname}</span></small>
        `;
    }
    document.getElementById("post_list").innerHTML = html;
})
.catch(error=>{
    console.error(error)
})
}
loadPost();