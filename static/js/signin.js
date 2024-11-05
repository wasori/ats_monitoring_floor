"use script";

const signin = document.getElementById("signin-bn");
const id = document.getElementById("user-id");
const pw = document.getElementById("user-pw");

signin.addEventListener("click", () => {
  if (id.value == "") {
    alert("아이디를 입력하세요.");
    id.focus();
    return false;
  }

  if (pw.value == "") {
    alert("비밀번호를 입력하세요.");
    pw.focus();
    return false;
  }

  // 서버에 로그인 정보를 전달
  fetch("/signin", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: id.value,
      pw: pw.value,
    }),
  })
    .then((response) => response.json()) // JSON 응답 받기
    .then((data) => {
      console.log(data);
      if (data.result === 1) {
        const hospitalName = data.hospital_name;
        window.location.href = `/main?hospital_name=${encodeURIComponent(
          hospitalName
        )}`;
      } else {
        alert("아이디 또는 비밀번호를 확인해주세요.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
