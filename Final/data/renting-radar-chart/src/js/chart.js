<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>租房数据雷达图</title>
    <link rel="stylesheet" href="styles.css"> <!-- 引入样式文件 -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script> <!-- 引入Chart.js -->
</head>
<body>
    <div class="container">
        <h1>租房数据雷达图</h1>
        <canvas id="radarChart"></canvas>
    </div>

    <script>
        const ctx = document.getElementById('radarChart').getContext('2d');
        const radarChart = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['面积', '房间数', '价格', '单价'], // 雷达图的标签
                datasets: [{
                    label: '租房数据',
                    data: [75.39, 2, 6600, 87.54], // 示例数据，您可以根据需要替换
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scale: {
                    ticks: {
                        beginAtZero: true
                    }
                }
            }
        });
    </script>
</body>
</html>