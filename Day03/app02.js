document.getElementById("form01").addEventListener("submit", function (event) {
    event.preventDefault();

    const name = document.getElementById("input_name").value;
    const age = document.getElementById("input_age").value;
    const email = document.getElementById("input_email").value;

    if (name.trim() === "" || age.trim() === "" || email.trim() === "") {
        alert("유효한 값을 채우세요.");
        return;
    }

    if (isNaN(age) || Number(age) <= 0) {
        alert("올바른 나이를 적으세요.");
        return;
    }

    document.getElementById("text_name").innerText = name;
    document.getElementById("text_age").innerText = age;
    document.getElementById("text_email").innerText = email;
});
