# ...existing code...
import pandas as pd
from pyecharts.charts import Radar
from pyecharts import options as opts

df = pd.read_csv('data/renting_origin.csv')
# 示例：统计各类型均值
values = [
    df['area'].mean(),
    df['room'].mean(),
    df['price'].mean(),
    df['unit_price'].mean()
]
schema = [
    {"name": "面积", "max": 200},
    {"name": "房间数", "max": 5},
    {"name": "价格", "max": 20000},
    {"name": "单价", "max": 200}
]

radar = Radar()
radar.add_schema(schema=schema)
radar.add("租房均值", [values])
radar.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
radar.set_global_opts(title_opts=opts.TitleOpts(title="租房数据雷达图"))
radar.render("image/renting_radar.html")
# ...existing code...