import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

base_csv_path = 'Data_process2/data/PEK.csv'

def data_process():

    # 读取数据
    df = pd.read_csv(base_csv_path)

    # 需要处理的列
    cols = ['HUMI', 'PRES', 'TEMP']

    # 线性插值
    df[cols] = df[cols].interpolate(method='linear', limit_direction='both')

    # 处理异常值
    for col in cols:
        mean = df[col].mean()
        std = df[col].std()
        upper = mean + 3 * std
        lower = mean - 3 * std
        df[col] = np.where(df[col] > upper, upper, df[col])
        df[col] = np.where(df[col] < lower, lower, df[col])

    # 保存新文件
    df.to_csv('Data_process2/data/achieves/PEK_interpolated.csv', index=False)

def pm_outlier_process(df):
    pm_cols = ['PM_Dongsi', 'PM_Dongsihuan', 'PM_Nongzhanguan']
    for col in pm_cols:
        df[col] = np.where(df[col] > 500, 500, df[col])
    return df

def cbwd_fill_cv(df):
    df['cbwd'] = df['cbwd'].mask(df['cbwd'] == 'cv').fillna(method='bfill')
    return df

def dew_temp_normalize_plot(df):
    # 0-1归一化
    for col in ['DEWP', 'TEMP']:
        df[f'{col}_minmax'] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
        df[f'{col}_zscore'] = (df[col] - df[col].mean()) / df[col].std()
    # 绘制散点图
    plt.figure(figsize=(10, 5))
    plt.scatter(df['DEWP_minmax'], df['TEMP_minmax'], s=5, label='MinMax')
    plt.scatter(df['DEWP_zscore'], df['TEMP_zscore'], s=5, label='Z-Score')
    plt.xlabel('DEWP')
    plt.ylabel('TEMP')
    plt.legend()
    plt.title('DEWP & TEMP Normalization Scatter')
    plt.savefig('Data_process2/data/achieves/dewp_temp_normalization.png')
    plt.close()

def air_quality_discretize(df):
    # AQI分级标准
    bins = [0, 50, 100, 150, 200, 300, 500]
    labels = ['优', '良', '轻度污染', '中度污染', '重度污染', '严重污染']
    # 以PM_Dongsi为例
    df['AQI_level'] = pd.cut(df['PM_Dongsi'], bins=bins, labels=labels, right=True)
    counts = df['AQI_level'].value_counts().sort_index()
    print('各空气质量级别天数：')
    print(counts)
    return counts

def process():
    df = pd.read_csv('Data_process2/data/PEK.csv')
    df = pm_outlier_process(df)
    df = cbwd_fill_cv(df)
    dew_temp_normalize_plot(df)
    air_quality_discretize(df)
    df.to_csv('Data_process2/data/achieves/PEK_processed.csv', index=False)

if __name__ == "__main__":
    process()