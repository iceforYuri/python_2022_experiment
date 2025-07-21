### 项目结构
```
/renting-dashboard
│
├── index.html
├── style.css
└── script.js
```

### 1. `index.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>租房数据雷达图</title>
    <link rel="stylesheet" href="style.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="container">
        <h1>租房数据雷达图</h1>
        <canvas id="radarChart"></canvas>
    </div>
    <script src="script.js"></script>
</body>
</html>
```

### 2. `style.css`
```css
body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    margin: 0;
    padding: 20px;
}

.container {
    max-width: 800px;
    margin: auto;
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h1 {
    text-align: center;
}
```

### 3. `script.js`
```javascript
const ctx = document.getElementById('radarChart').getContext('2d');

// 示例数据，您可以根据实际数据进行调整
const labels = ['房间数', '面积', '价格', '单价'];
const data = {
    labels: labels,
    datasets: [{
        label: '租房数据',
        data: [3, 100, 9600, 96], // 示例数据
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1
    }]
};

const config = {
    type: 'radar',
    data: data,
    options: {
        scales: {
            r: {
                beginAtZero: true
            }
        }
    }
};

const radarChart = new Chart(ctx, config);
```

### 说明
1. **HTML文件**: `index.html`是项目的主文件，包含了Chart.js库的引用和一个canvas元素用于绘制雷达图。
2. **CSS文件**: `style.css`用于设置页面的基本样式。
3. **JavaScript文件**: `script.js`中包含了绘制雷达图的逻辑。您需要根据实际的租房数据来填充`data`数组。

### 数据处理
您需要将CSV数据转换为适合雷达图的数据格式。可以使用JavaScript读取CSV文件并解析数据，或者手动将数据填入`data`数组中。

### 运行项目
1. 将上述文件保存到相应的文件中。
2. 使用浏览器打开`index.html`文件，即可查看雷达图。

根据您的需求，您可以进一步美化样式或添加更多功能。