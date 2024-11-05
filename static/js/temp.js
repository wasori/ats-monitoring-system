
// fetchData 함수 정의
function fetchtemp() {
    fetch('/temp_data')
        .then(response => response.json())  // JSON 형식으로 응답 파싱
        .then(data => {
            const temDetail = document.querySelector('.tem-detail');
            const snapshotDiv = document.querySelector('.tem-photo');
            const temperatureDiv = document.querySelector('.tem-temp');
            const temtimeDiv = document.querySelector('.tem-time');
            // console.log(data)

            temDetail.innerHTML = '';  // 기존 데이터를 초기화

            // 데이터를 가장 최근 항목부터 정렬 (내림차순)
            data.sort((b, a) => new Date(b.uptime) - new Date(a.uptime));
            
            // 데이터를 한 줄씩 추가
            data.forEach(item => {
                const detailLine = document.createElement('div');
                detailLine.textContent = `ID: ${item.robot_id}, Temp: ${item.temperature}, Person ID: ${item.personid}`;
                detailLine.classList.add('item'); // 각 항목에 클래스 추가
                detailLine.dataset.snapshot = item.snapshot; // snapshot 데이터를 data attribute로 저장

                // 클릭 이벤트 리스너 추가
                detailLine.addEventListener('click', () => {
                    const snapshotData = `data:image/png;base64,${item.snapshot}`;
                    snapshotDiv.style.backgroundImage = `url(${snapshotData})`; // 클릭한 항목의 snapshot으로 이미지 변경
                    // 온도 데이터를 표시
                    temperatureDiv.innerText = `${item.temperature} °C`;
                    temtimeDiv.innerText = `${item.uptime}`;
                });
                
                temDetail.insertBefore(detailLine, temDetail.firstChild);

                
            });  // 예시로 JSON 데이터를 tem-detail에 표시

            // 초기값으로 첫 번째 항목의 snapshot과 온도 데이터 표시 (선택 사항)
            // 가장 최근의 항목을 찾아 초기값으로 표시
            if (data.length > 0) {
                const mostRecentItem = data.reduce((prev, current) => {
                    return new Date(prev.uptime) > new Date(current.uptime) ? prev : current;
                });
                const snapshotData = `data:image/png;base64,${mostRecentItem.snapshot}`;
                snapshotDiv.style.backgroundImage = `url(${snapshotData})`;
                temperatureDiv.innerText = `${mostRecentItem.temperature} °C`; // 초기값으로 가장 최근 항목의 온도 데이터 표시
                temtimeDiv.innerText = `${mostRecentItem.uptime}`;
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

fetchtemp()

setInterval(fetchtemp,5000)
setInterval(fetchData, 5000);
// setInterval(fetch_sensor,5000);
// setInterval(fetch_vision,5000);
// setInterval(fetch_robot,5000);