document.addEventListener('DOMContentLoaded', () => {
    // 병동 등록 모달 열기 및 닫기
    const openModalButton = document.getElementById('open-modal');
    const closeModalButton = document.getElementById('close-modal');
    const modalOverlay = document.getElementById('modal-overlay');

    openModalButton.addEventListener('click', () => {
        modalOverlay.style.display = 'flex';
    });

    closeModalButton.addEventListener('click', () => {
        modalOverlay.style.display = 'none';
    });

    // 병동 등록 폼 제출
    document.getElementById('ward-form').addEventListener('submit', async (event) => {
        event.preventDefault(); // 기본 동작 막기
        const formData = new FormData(event.target);

        // URL 파라미터에서 hospital_name 가져오기
        const hospitalName = new URLSearchParams(window.location.search).get('hospital_name');

        // 서버로 보낼 데이터 준비
        const requestData = {
            hospital_name: formData.get('hospital-name'),
            ward: formData.get('ward-name'),
            room: formData.get('room-number'),
            ward_photo: formData.get('ward-photo'),
            hospital_id: hospitalName
        };

        try {
            // 서버로 POST 요청
            const response = await fetch('/input_hospital_regist', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData),
            });
    
            const result = await response.json();
    
            if (response.ok) {
                alert('병동 등록 완료!');
                modalOverlay.style.display = 'none';
            } else {
                alert(`에러 발생: ${result.error || '알 수 없는 오류'}`);
            }
        } catch (error) {
            alert(`요청 중 오류가 발생했습니다: ${error.message}`);
        }
    });

    // 로봇 목록 모달 열기 및 닫기
    const openRobotModalButton = document.querySelector('.admin-button:nth-child(2)');
    const closeRobotModalButton = document.getElementById('close-robot-modal');
    const robotModalOverlay = document.getElementById('robot-modal-overlay');
    const robotTableBody = document.getElementById('robot-table-body');

    const openRegisterModalButton = document.getElementById('open-register-modal');
    const robotRegistModalOverlay = document.getElementById('robot-regist-modal-overlay')
    const closeRobotRegistButton = document.getElementById('go-back-to-list')

    const hospitalName = new URLSearchParams(window.location.search).get('hospital_name');

    openRobotModalButton.addEventListener('click', async () => {
        try {
            const response = await fetch(`/get_robo_regist?hospital_name=${hospitalName}`);
            const data = await response.json();

            robotTableBody.innerHTML = ''; // 기존 데이터 초기화
            data.forEach((robot) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${robot.robot_id}</td>
                    <td>${robot.hospital_name}</td>
                    <td>${robot.ward}</td>
                    <td>${robot.room}</td>
                    <td>${robot.state}</td>
                    <td>${robot.regist_date}</td>
                `;

                // 마우스 호버 이벤트
            row.addEventListener('mouseover', () => {
                row.style.backgroundColor = '#f0f0f0'; // 색상 진하게
            });
            row.addEventListener('mouseout', () => {
                row.style.backgroundColor = ''; // 원래 색상으로 복구
            });

            // 클릭 이벤트
            row.addEventListener('click', () => {
                document.getElementById('robot-id').value = robot.robot_id;
                document.getElementById('hospital-name-regist').value = robot.hospital_name;
                document.getElementById('ward').value = robot.ward;
                document.getElementById('room').value = robot.room;
                document.getElementById('state').value = robot.state;
                document.getElementById('hospital-id').value = robot.hospital_id;

                // 등록 창 띄우기
                document.getElementById('"robot-register-modal').style.display = 'flex';
            });
                robotTableBody.appendChild(row);
            });

            robotModalOverlay.style.display = 'flex';
        } catch (error) {
            console.error('데이터를 가져오는 중 오류 발생:', error);
        }
    });

    closeRobotModalButton.addEventListener('click', () => {
        robotModalOverlay.style.display = 'none';
    });

    openRegisterModalButton.addEventListener('click', ()=>{
        robotRegistModalOverlay.style.display = 'flex'
        robotModalOverlay.style.display = 'none';
    })

    closeRobotRegistButton.addEventListener('click', ()=>{
        robotRegistModalOverlay.style.display = 'none'
        robotModalOverlay.style.display = 'flex';
    })
    
    document.getElementById('robot-register-form').addEventListener('submit', async (event) => {
        event.preventDefault(); // 폼 기본 제출 방지

        const robotId = document.getElementById('robot-id').value;
        const hospital_Name = document.getElementById('hospital-name-regist').value;
        const ward = document.getElementById('ward').value;
        const room = document.getElementById('room').value;
        const state = document.getElementById('state').value;

        const requestData = {
            robot_id: robotId,
            hospital_name: hospital_Name,
            ward: ward,
            room: room,
            state: state,
            hospital_id: hospitalName
        };

        try {
            const response = await fetch('/input_robo_regist', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData),
            });
    
            const result = await response.json();
            if (response.ok) {
                alert(result.message);
            } else {
                alert('등록 실패: ' + result.error); // 중복 알림 포함
            }
        } catch (error) {
            console.error(error);
            alert('서버 오류가 발생했습니다.');
        }
    });
});


