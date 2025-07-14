import pandas as pd
import matplotlib.pyplot as plt
import os

# 设置中文字体（Windows 推荐使用 SimHei）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

CSV_PATH = 'Data_process1/Data/result.csv'

def plot_price_distribution(csv_path, save_path='Data_process/images/new_house_price_distribution.png'):
    # 读取数据
    df = pd.read_csv(csv_path)
    # 去除价格待定和缺失数据
    df = df[df['sigle_price'].apply(lambda x: str(x).replace('价格待定', '').strip() != '')]
    df = df[df['total_price'].apply(lambda x: str(x).strip() != '')]
    # 处理价格区间（取区间中位数）
    def parse_price(price):
        if '-' in str(price):
            parts = str(price).split('-')
            try:
                return (float(parts[0]) + float(parts[1])) / 2
            except:
                return None
        try:
            return float(price)
        except:
            return None
    df['sigle_price'] = df['sigle_price'].apply(parse_price)
    df['total_price'] = df['total_price'].apply(parse_price)
    df = df.dropna(subset=['sigle_price', 'total_price', 'type'])

    # 绘制散点图
    plt.figure(figsize=(10, 6))
    types = df['type'].unique()
    cmap = plt.colormaps['tab10']
    for idx, t in enumerate(types):
        sub_df = df[df['type'] == t]
        plt.scatter(sub_df['sigle_price'], sub_df['total_price'], label=t, color=cmap(idx))
    plt.xlabel('单价（元/㎡）')
    plt.ylabel('总价（万元）')
    plt.title('楼盘价格分布')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()



def plot_district_histograms(csv_path, save_dir='Data_process/images'):
    import numpy as np
    os.makedirs(save_dir, exist_ok=True)
    df = pd.read_csv(csv_path)
    df = df[df['sigle_price'].apply(lambda x: str(x).replace('价格待定', '').strip() != '')]
    df = df[df['total_price'].apply(lambda x: str(x).strip() != '')]

    def parse_price(price):
        if '-' in str(price):
            parts = str(price).split('-')
            try:
                return (float(parts[0]) + float(parts[1])) / 2
            except:
                return None
        try:
            return float(price)
        except:
            return None

    df['sigle_price'] = df['sigle_price'].apply(parse_price)
    df['total_price'] = df['total_price'].apply(parse_price)
    df = df.dropna(subset=['sigle_price', 'total_price', 'position'])
    df['district'] = df['position'].apply(lambda x: str(x).split('/')[0])

    grouped = df.groupby('district')
    districts = []
    avg_sigle_prices = []
    avg_total_prices = []
    counts = []
    for name, group in grouped:
        districts.append(name)
        avg_sigle_prices.append(group['sigle_price'].mean())
        avg_total_prices.append(group['total_price'].mean())
        counts.append(len(group))

    # 颜色映射
    cmap = plt.colormaps['Set3']
    colors = [cmap(i) for i in range(len(districts))]
    bar_widths = np.array(counts)
    lefts = np.concatenate(([0], np.cumsum(bar_widths)[:-1]))

    # ...existing code...
    # 平均单价直方图
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(lefts, avg_sigle_prices, width=bar_widths, color=colors, edgecolor='black', align='edge')
    ax.set_xlabel('累计楼盘数量')
    ax.set_ylabel('平均单价/元')
    ax.set_title('各行政区楼盘平均单价及数量（宽度代表数量）')
    xticks = np.concatenate((lefts, [lefts[-1] + bar_widths[-1]]))
    ax.set_xticks(xticks)
    ax.set_xticklabels([str(int(x)) for x in xticks])
    ax.legend(bars, districts, loc='upper right', bbox_to_anchor=(1.15, 1))
    # 关键：设置x轴范围，左端为0，右端为最后一个柱子的右端
    ax.set_xlim(0, lefts[-1] + bar_widths[-1])
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'district_avg_sigle_price_hist.png'), dpi=300)
    plt.close()

    # 平均总价直方图
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(lefts, avg_total_prices, width=bar_widths, color=colors, edgecolor='black', align='edge')
    ax.set_xlabel('累计楼盘数量')
    ax.set_ylabel('平均总价/万元')
    ax.set_title('各行政区楼盘平均总价及数量（宽度代表数量）')
    xticks = np.concatenate((lefts, [lefts[-1] + bar_widths[-1]]))
    ax.set_xticks(xticks)
    ax.set_xticklabels([str(int(x)) for x in xticks])
    ax.legend(bars, districts, loc='upper right', bbox_to_anchor=(1.15, 1))
    ax.set_xlim(0, lefts[-1] + bar_widths[-1])
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'district_avg_total_price_hist.png'), dpi=300)
    plt.close()

# 示例调用
if __name__ == "__main__":
    plot_price_distribution(CSV_PATH)
    plot_district_histograms(CSV_PATH)