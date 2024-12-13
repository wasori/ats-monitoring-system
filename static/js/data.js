let chartInstance; // 차트 인스턴스 관리

// 기본 그래프 데이터 가져오기
async function fetchdbData() {
    const response = await fetch('/get_content_stats');
    const data = await response.json();

    // 데이터 가공
    const labels = data.map(item => item.content);
    const counts = data.map(item => item.count);

    // Chart.js로 그래프 그리기
    const ctx = document.getElementById('contentChart').getContext('2d');

    // 기존 차트 제거
    if (chartInstance) {
        chartInstance.destroy();
    }

    // 새 차트 생성
    chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: '상황별 통계',
                data: counts,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// 날짜별 데이터 가져오기
async function fetchStatsByDate(content) {
    const response = await fetch(`/get_content_stats_by_date?content=${content}`);
    const data = await response.json();

    if (data.error) {
        console.error(data.error);
        return;
    }

    // 데이터 가공
    const labels = data.map(item => item.date);
    const counts = data.map(item => item.count);

    // Chart.js로 그래프 그리기
    const ctx = document.getElementById('contentChart').getContext('2d');

    // 기존 차트 제거
    if (chartInstance) {
        chartInstance.destroy();
    }

    // 새 차트 생성
    chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: `${content} 통계 (날짜별)`,
                data: counts,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// 버튼 클릭 이벤트 추가
document.querySelectorAll('.data-left button').forEach(button => {
    button.addEventListener('click', () => {
        const content = button.textContent.trim(); // 버튼 텍스트로 content 결정
        const contentMap = {
            '전체': '', // 전체는 특별한 content가 없음
            '욕창': 'pose',
            '낙상': 'down',
            '먼지감지': 'dust',
            '물감지': 'water',
            '화재감지': 'fire'
        };

        if (content === '전체') {
            fetchdbData(); // 기본 그래프
        } else {
            fetchStatsByDate(contentMap[content]); // 날짜별 그래프
        }
    });
});

// 페이지 로드 시 기본 그래프 표시
fetchdbData();
