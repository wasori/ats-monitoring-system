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
    document.getElementById('ward-form').addEventListener('submit', (event) => {
        event.preventDefault(); // 기본 동작 막기
        const formData = new FormData(event.target);

        console.log({
            hospitalName: formData.get('hospital-name'),
            wardName: formData.get('ward-name'),
            roomNumber: formData.get('room-number'),
            wardPhoto: formData.get('ward-photo'),
        });

        alert('병동 등록 완료!');
        modalOverlay.style.display = 'none';
    });

    // 로봇 목록 모달 열기 및 닫기
    const openRobotModalButton = document.querySelector('.admin-button:nth-child(2)');
    const closeRobotModalButton = document.getElementById('close-robot-modal');
    const robotModalOverlay = document.getElementById('robot-modal-overlay');
    const robotTableBody = document.getElementById('robot-table-body');

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
    
});


