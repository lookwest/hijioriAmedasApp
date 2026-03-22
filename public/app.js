
document.addEventListener('DOMContentLoaded', () => {
    const DATA_URL = 'hijioriAmedas_data_utf8.csv';
    const CHART_EL = document.getElementById('weatherChart');
    const LATEST_TEMP_EL = document.getElementById('latestTemp');
    const LATEST_SNOW_EL = document.getElementById('latestSnow');
    const TODAY_MAX_EL = document.getElementById('todayMaxTemp');
    const TODAY_MIN_EL = document.getElementById('todayMinTemp');
    const LAST_UPDATE_EL = document.getElementById('lastUpdate');

    let weatherChart = null;

    async function fetchDataAndDrawChart() {
        try {
            const response = await fetch(DATA_URL);
            if (!response.ok) {
                throw new Error(`データの取得に失敗しました: ${response.statusText}`);
            }
            const csvText = await response.text();
            
            // CSVデータをパース (簡易的なパース。本番ではライブラリ推奨だが、この規模なら分割で対応)
            const rows = csvText.trim().split('\n');
            const headers = rows[0].split(',');
            const data = rows.slice(1).map(row => {
                const values = row.split(',');
                let rowData = {};
                headers.forEach((header, index) => {
                    const h = header.trim();
                    rowData[h] = values[index] ? values[index].trim() : null;
                });
                return rowData;
            });

            // 必要な列名
            const H_DATE = '年月日';
            const H_MAX_TEMP = '最高気温(℃)';
            const H_MIN_TEMP = '最低気温(℃)';
            const H_AVG_TEMP = '平均気温(℃)';
            const H_SNOW_DEPTH = '最深積雪(cm)';
            const H_PRECIP = '降水量の合計(mm)';

            // 最新データの更新
            const latest = data[data.length - 1];
            if (latest) {
                LATEST_TEMP_EL.innerHTML = `${latest[H_AVG_TEMP] || '--'}<span class="unit">℃</span>`;
                LATEST_SNOW_EL.innerHTML = `${latest[H_SNOW_DEPTH] || '0'}<span class="unit">cm</span>`;
                TODAY_MAX_EL.innerHTML = `${latest[H_MAX_TEMP] || '--'}<span class="unit">℃</span>`;
                TODAY_MIN_EL.innerHTML = `${latest[H_MIN_TEMP] || '--'}<span class="unit">℃</span>`;
                LAST_UPDATE_EL.textContent = `最終更新データ: ${latest[H_DATE]}`;
            }

            // 直近30日のデータをフィルタリング
            const endDate = new Date();
            const startDate = dateFns.subDays(endDate, 30);

            const filteredData = data.filter(d => {
                const date = dateFns.parse(d[H_DATE], 'yyyy/M/d', new Date());
                return dateFns.isWithinInterval(date, { start: startDate, end: endDate });
            });

            // Chart.js用のデータ形式に変換
            const labels = filteredData.map(d => dateFns.format(dateFns.parse(d[H_DATE], 'yyyy/M/d', new Date()), 'M/d'));
            const maxTempData = filteredData.map(d => parseFloat(d[H_MAX_TEMP]) || null);
            const minTempData = filteredData.map(d => parseFloat(d[H_MIN_TEMP]) || null);
            const snowData = filteredData.map(d => parseFloat(d[H_SNOW_DEPTH]) || 0);
            const precipData = filteredData.map(d => parseFloat(d[H_PRECIP]) || 0);
            
            // グラフを描画
            const isMobile = window.innerWidth < 768;
            
            if (weatherChart) {
                weatherChart.destroy();
            }

            weatherChart = new Chart(CHART_EL, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: '降水量(mm)',
                            data: precipData,
                            type: 'bar',
                            yAxisID: 'y-axis-right',
                            backgroundColor: 'rgba(41, 128, 185, 0.5)',
                            borderColor: 'rgba(41, 128, 185, 0.8)',
                            borderWidth: 1,
                            order: 3
                        },
                        {
                            label: '積雪深(cm)',
                            data: snowData,
                            type: 'line',
                            yAxisID: 'y-axis-right',
                            backgroundColor: 'rgba(149, 165, 166, 0.2)',
                            borderColor: 'rgba(149, 165, 166, 0.6)',
                            borderWidth: 2,
                            fill: true,
                            pointRadius: 0,
                            order: 4,
                            tension: 0.1
                        },
                        {
                            label: '最高気温(℃)',
                            data: maxTempData,
                            type: 'line',
                            yAxisID: 'y-axis-temp',
                            borderColor: '#e74c3c',
                            backgroundColor: '#e74c3c',
                            pointRadius: isMobile ? 2 : 3,
                            borderWidth: 2,
                            tension: 0.3,
                            order: 1
                        },
                        {
                            label: '最低気温(℃)',
                            data: minTempData,
                            type: 'line',
                            yAxisID: 'y-axis-temp',
                            borderColor: '#3498db',
                            backgroundColor: '#3498db',
                            pointRadius: isMobile ? 2 : 3,
                            borderWidth: 2,
                            tension: 0.3,
                            order: 2
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {
                        mode: 'index',
                        intersect: false,
                    },
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                boxWidth: 12,
                                padding: 15,
                                font: {
                                    size: isMobile ? 10 : 12
                                }
                            }
                        },
                        tooltip: {
                            backgroundColor: 'rgba(255, 255, 255, 0.9)',
                            titleColor: '#2c3e50',
                            bodyColor: '#2c3e50',
                            borderColor: '#ddd',
                            borderWidth: 1,
                            padding: 10,
                        }
                    },
                    scales: {
                        'y-axis-temp': {
                            type: 'linear',
                            position: 'left',
                            title: {
                                display: !isMobile,
                                text: '気温 (℃)'
                            },
                            ticks: {
                                font: { size: isMobile ? 10 : 11 }
                            }
                        },
                        'y-axis-right': {
                            type: 'linear',
                            position: 'right',
                            title: {
                                display: !isMobile,
                                text: '降水/積雪'
                            },
                            grid: {
                                drawOnChartArea: false,
                            },
                            beginAtZero: true,
                            ticks: {
                                font: { size: isMobile ? 10 : 11 }
                            }
                        },
                        x: {
                           ticks: {
                                font: { size: isMobile ? 9 : 11 },
                                maxRotation: 45,
                                autoSkip: true,
                                maxTicksLimit: isMobile ? 10 : 15
                           }
                        }
                    }
                }
            });

        } catch (error) {
            console.error('エラーが発生しました:', error);
            LAST_UPDATE_EL.textContent = 'データの読み込みに失敗しました。';
        }
    }

    fetchDataAndDrawChart();

    // リサイズ時にグラフを再描画してレスポンシブ対応を確実に
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            fetchDataAndDrawChart();
        }, 250);
    });
});
