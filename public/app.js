
document.addEventListener('DOMContentLoaded', () => {
    const DATA_URL = 'hijioriAmedas_data_utf8.csv';
    const CHART_EL = document.getElementById('weatherChart');

    async function fetchDataAndDrawChart() {
        try {
            const response = await fetch(DATA_URL);
            if (!response.ok) {
                throw new Error(`データの取得に失敗しました: ${response.statusText}`);
            }
            const csvText = await response.text();
            
            // CSVデータをパース
            const rows = csvText.trim().split('\n');
            const headers = rows[0].split(',');
            const data = rows.slice(1).map(row => {
                const values = row.split(',');
                let rowData = {};
                headers.forEach((header, index) => {
                    rowData[header.trim()] = values[index] ? values[index].trim() : null;
                });
                return rowData;
            });

            // 必要な列のインデックスを取得
            const dateHeader = '年月日';
            const maxTempHeader = '最高気温(℃)';
            const minTempHeader = '最低気温(℃)';
            const snowDepthHeader = '最深積雪(cm)';

            // 直近1ヶ月のデータをフィルタリング
            const endDate = new Date();
            const startDate = dateFns.subDays(endDate, 30);

            const filteredData = data.filter(d => {
                const date = dateFns.parse(d[dateHeader], 'yyyy/M/d', new Date());
                return dateFns.isWithinInterval(date, { start: startDate, end: endDate });
            });

            // Chart.js用のデータ形式に変換
            const labels = filteredData.map(d => dateFns.format(dateFns.parse(d[dateHeader], 'yyyy/M/d', new Date()), 'M/d'));
            const maxTempData = filteredData.map(d => parseFloat(d[maxTempHeader]) || null);
            const minTempData = filteredData.map(d => parseFloat(d[minTempHeader]) || null);
            const snowData = filteredData.map(d => parseFloat(d[snowDepthHeader]) || null);
            
            // グラフを描画
            new Chart(CHART_EL, {
                type: 'bar', // 複合グラフのベースタイプ
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: '最深積雪 (cm)',
                            data: snowData,
                            type: 'bar',
                            yAxisID: 'y-axis-snow',
                            backgroundColor: 'rgba(173, 216, 230, 0.6)',
                            borderColor: 'rgba(173, 216, 230, 1)',
                            borderWidth: 1
                        },
                        {
                            label: '最高気温 (℃)',
                            data: maxTempData,
                            type: 'line',
                            yAxisID: 'y-axis-temp',
                            borderColor: 'rgba(255, 99, 132, 1)',
                            backgroundColor: 'rgba(255, 99, 132, 0.2)',
                            tension: 0.1
                        },
                        {
                            label: '最低気温 (℃)',
                            data: minTempData,
                            type: 'line',
                            yAxisID: 'y-axis-temp',
                            borderColor: 'rgba(54, 162, 235, 1)',
                            backgroundColor: 'rgba(54, 162, 235, 0.2)',
                            tension: 0.1
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    scales: {
                        'y-axis-temp': {
                            type: 'linear',
                            position: 'left',
                            title: {
                                display: true,
                                text: '気温 (℃)'
                            }
                        },
                        'y-axis-snow': {
                            type: 'linear',
                            position: 'right',
                            title: {
                                display: true,
                                text: '最深積雪 (cm)'
                            },
                            grid: {
                                drawOnChartArea: false, // 気温のグリッドと重ならないように
                            },
                            beginAtZero: true
                        },
                        x: {
                           ticks: {
                                maxRotation: 70,
                                minRotation: 70
                           }
                        }
                    }
                }
            });

        } catch (error) {
            console.error('エラーが発生しました:', error);
            CHART_EL.getContext('2d').fillText('グラフの読み込みに失敗しました。', 10, 50);
        }
    }

    fetchDataAndDrawChart();
});
