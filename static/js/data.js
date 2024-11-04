// fetchData 함수 정의
function fetch_sensor() {
    fetch('/sensor_data')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // JSON 형식으로 응답 파싱
        })
        .then(data => {
            const dataBox = document.querySelector('.data-box');
            dataBox.innerHTML = ''; // 기존 데이터를 초기화

            // 데이터를 한 줄씩 추가
            data.forEach(item => {
                const sensorLine = document.createElement('div');
                sensorLine.classList.add('sensor-item'); // 각 항목에 클래스 추가
                sensorLine.textContent = `Robot ID: ${item.robot_id}, Dust: ${item.dust}, Water: ${item.water}, Fire: ${item.fire}, Time: ${item.uptime}`;
                
                // 리스트를 data-box에 추가
                dataBox.insertBefore(sensorLine, dataBox.firstChild);
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error); // 오류 처리
        });
}

// fetchData 함수 정의
function fetch_vision() {
    fetch('/vision_data')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // JSON 형식으로 응답 파싱
        })
        .then(data => {
            const dataBox = document.getElementById('vision');
            dataBox.innerHTML = ''; // 기존 데이터를 초기화

            // 데이터를 한 줄씩 추가
            data.forEach(item => {
                const visionLine = document.createElement('div');
                visionLine.classList.add('vision-item'); // 각 항목에 클래스 추가
                visionLine.textContent = `Robot ID: ${item.robot_id}, Room: ${item.room}, Sickbed: ${item.sickbed}, Pose: ${item.pose}, uptime: ${item.uptime}`;
                
                // 리스트를 data-box에 추가
                dataBox.insertBefore(visionLine, dataBox.firstChild);
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error); // 오류 처리
        });
}

function fetch_robot() {
    fetch('/robot_data')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // JSON 형식으로 응답 파싱
        })
        .then(data => {
            const dataBox = document.getElementById('robot');
            dataBox.innerHTML = ''; // 기존 데이터를 초기화

            // 데이터를 한 줄씩 추가
            data.forEach(item => {
                const robotLine = document.createElement('div');
                robotLine.classList.add('robot-item'); // 각 항목에 클래스 추가
                robotLine.textContent = `Robot ID: ${item.robot_id}, xaxis: ${item.xaxis}, yaxis: ${item.yaxis}, uptime: ${item.uptime}`;
                
                // 리스트를 data-box에 추가
                dataBox.insertBefore(robotLine, dataBox.firstChild);
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error); // 오류 처리
        });
}