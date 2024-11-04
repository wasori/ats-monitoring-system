document.addEventListener("DOMContentLoaded", function() {
  const idInput = document.querySelector('.id');
  const passInput = document.querySelector('.pass');

  idInput.addEventListener('focus', function() {
      this.setAttribute('placeholder', ''); // 포커스 시 placeholder 비우기
  });

  idInput.addEventListener('blur', function() {
      if (this.value === '') {
          this.setAttribute('placeholder', '아이디 입력'); // 입력 필드가 비어있으면 placeholder 다시 설정
      }
  });

  passInput.addEventListener('focus', function() {
      this.setAttribute('placeholder', ''); // 포커스 시 placeholder 비우기
  });

  passInput.addEventListener('blur', function() {
      if (this.value === '') {
          this.setAttribute('placeholder', '비밀번호 입력'); // 입력 필드가 비어있으면 placeholder 다시 설정
      }
  });
});

function signin() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  // 빈 칸 체크
  if (username === "") {
    alert("아이디를 입력해주세요.");
    return;
  }
  if (password === "") {
    alert("비밀번호를 입력해주세요.");
    return;
  }

  // 서버에 로그인 정보를 전달
  fetch('/signin', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      id: username,
      pw: password,
    }),
  })
  .then(response => response.json())  // JSON 응답 받기
  .then(data => {
    console.log(data)
    if (data.result === 1) {
      const hospitalName = data.hospital_name;
      window.location.href = `/main?hospital_name=${encodeURIComponent(hospitalName)}`;
    } else {
      alert("아이디 또는 비밀번호를 확인해주세요.");
    }
  })
  .catch((error) => {
    console.error('Error:', error);
  });
}