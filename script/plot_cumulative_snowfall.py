import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# データファイルを読み込む
file_path = 'hijioriAmedas_data_utf8.csv'
df = pd.read_csv(file_path, encoding='utf-8', na_values=['', ' ', '--', '×', '#'])

# '年月日'列をdatetime型に変換
df['年月日'] = pd.to_datetime(df['年月日'], errors='coerce')

# '降雪量合計(cm)'列を数値に変換し、NaNを0に置換
df['降雪量合計(cm)'] = pd.to_numeric(df['降雪量合計(cm)'], errors='coerce').fillna(0)

# 今年の期間 (12/1 - 1/4)
this_year_end_date = datetime(2026, 1, 4) # 昨日
this_year_start_date = datetime(2025, 12, 1)
mask_this_year = (df['年月日'] >= this_year_start_date) & (df['年月日'] <= this_year_end_date)
df_this_year = df.loc[mask_this_year].copy()
df_this_year['累積降雪量(cm)'] = df_this_year['降雪量合計(cm)'].cumsum()
df_this_year['経過日数'] = (df_this_year['年月日'] - datetime(df_this_year['年月日'].iloc[0].year, 12, 1)).dt.days

# 昨年の期間 (12/1 - 1/4)
last_year_end_date = datetime(2025, 1, 4)
last_year_start_date = datetime(2024, 12, 1)
mask_last_year = (df['年月日'] >= last_year_start_date) & (df['年月日'] <= last_year_end_date)
df_last_year = df.loc[mask_last_year].copy()
df_last_year['累積降雪量(cm)'] = df_last_year['降雪量合計(cm)'].cumsum()
df_last_year['経過日数'] = (df_last_year['年月日'] - datetime(df_last_year['年月日'].iloc[0].year, 12, 1)).dt.days

# グラフ描画
plt.style.use('default')
plt.rcParams['font.sans-serif'] = ['Hiragino Sans']
plt.rcParams['axes.grid'] = True

fig, ax = plt.subplots(figsize=(12, 8))

# 今年の累積降雪量
ax.plot(df_this_year['経過日数'], df_this_year['累積降雪量(cm)'], marker='o', linestyle='-', label='今年 (2025/12/01 - 2026/01/04)', color='tab:red')

# 昨年の累積降雪量
ax.plot(df_last_year['経過日数'], df_last_year['累積降雪量(cm)'], marker='x', linestyle='--', label='昨年 (2024/12/01 - 2025/01/04)', color='tab:blue')


ax.set_xlabel('12月1日からの経過日数')
ax.set_ylabel('累積降雪量 (cm)')
ax.set_title('12月から昨日までの累積降雪量比較')
ax.legend()
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
# ax.tick_params(axis='x', rotation=45)

# Y軸の範囲を調整 (最大累積値の少し上まで)
max_cumulative_snow = max(df_this_year['累積降雪量(cm)'].max(), df_last_year['累積降雪量(cm)'].max())
ax.set_ylim(0, max_cumulative_snow * 1.1)
ax.set_xlim(0, 35) # X軸の範囲を12月1日からの経過日数で設定
ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True)) # X軸の目盛りを整数にする


fig.tight_layout()
output_path = 'img/cumulative_snowfall_comparison.png'
plt.savefig(output_path)

print(f"グラフを {output_path} に保存しました。")
print(f"df_this_year['経過日数'] head:\n{df_this_year['経過日数'].head()}")
print(f"df_this_year['経過日数'] dtype: {df_this_year['経過日数'].dtype}")
print(f"df_last_year['経過日数'] head:\n{df_last_year['経過日数'].head()}")
print(f"df_last_year['経過日数'] dtype: {df_last_year['経過日数'].dtype}")