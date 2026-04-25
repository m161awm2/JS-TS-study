document.getElementById("myForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const name = document.getElementById("input_name").value;
    const age = document.getElementById("input_age").value;
    const content = document.getElementById("input_content").value;

    if (name.trim().length < 2) {
        alert("이름은 두 글자 이상 입력하세요.");
        return;
    }

    if (isNaN(age) || age.trim() === "") {
        alert("나이는 숫자로 입력하세요.");
        return;
    }

    if (content.trim().length < 5) {
        alert("내용은 5글자 이상 입력하세요.");
        return;
    }

    document.getElementById("text_name").innerText = name;
    document.getElementById("text_age").innerText = age;
    document.getElementById("text_content").innerText = content;
});
