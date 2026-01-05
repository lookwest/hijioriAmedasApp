
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from datetime import datetime, timedelta

# データファイルを読み込む
file_path = 'hijioriAmedas_data_utf8.csv'
df = pd.read_csv(file_path, encoding='utf-8', na_values=['', ' ', '--', '×', '#'])

# '年月日'列をdatetime型に変換
df['年月日'] = pd.to_datetime(df['年月日'], errors='coerce')

# '降水量の合計(mm)'列を数値に変換し、NaNを0に置換
df['降水量の合計(mm)'] = pd.to_numeric(df['降水量の合計(mm)'], errors='coerce').fillna(0)

# 今年の期間 (12/1 - 1/4)
this_year_end_date = datetime(2026, 1, 4) # 昨日
this_year_start_date = datetime(2025, 12, 1)
mask_this_year = (df['年月日'] >= this_year_start_date) & (df['年月日'] <= this_year_end_date)
df_this_year = df.loc[mask_this_year].copy()
df_this_year['累積降水量(mm)'] = df_this_year['降水量の合計(mm)'].cumsum()
df_this_year['経過日数'] = (df_this_year['年月日'] - datetime(df_this_year['年月日'].iloc[0].year, 12, 1)).dt.days

# 昨年の期間 (12/1 - 1/4)
last_year_end_date = datetime(2025, 1, 4)
last_year_start_date = datetime(2024, 12, 1)
mask_last_year = (df['年月日'] >= last_year_start_date) & (df['年月日'] <= last_year_end_date)
df_last_year = df.loc[mask_last_year].copy()
df_last_year['累積降水量(mm)'] = df_last_year['降水量の合計(mm)'].cumsum()
df_last_year['経過日数'] = (df_last_year['年月日'] - datetime(df_last_year['年月日'].iloc[0].year, 12, 1)).dt.days

# グラフ描画
plt.style.use('default')
plt.rcParams['font.sans-serif'] = ['Hiragino Sans']
plt.rcParams['axes.grid'] = True

fig, ax = plt.subplots(figsize=(12, 8))

# 今年の累積降水量
ax.plot(df_this_year['経過日数'], df_this_year['累積降水量(mm)'], marker='o', linestyle='-', label='今年 (2025/12/01 - 2026/01/04)', color='tab:red')

# 昨年の累積降水量
ax.plot(df_last_year['経過日数'], df_last_year['累積降水量(mm)'], marker='x', linestyle='--', label='昨年 (2024/12/01 - 2025/01/04)', color='tab:blue')


ax.set_xlabel('12月1日からの経過日数')
ax.set_ylabel('累積降水量 (mm)')
ax.set_title('12月から昨日までの累積降水量比較')
ax.legend()

# Y軸の範囲を調整 (最大累積値の少し上まで)
max_cumulative_precip = max(df_this_year['累積降水量(mm)'].max(), df_last_year['累積降水量(mm)'].max())
ax.set_ylim(0, max_cumulative_precip * 1.1)
ax.set_xlim(0, 35) # X軸の範囲を12月1日からの経過日数で設定
ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True)) # X軸の目盛りを整数にする


fig.tight_layout()
output_path = 'img/cumulative_precipitation_comparison.png'
plt.savefig(output_path)

print(f"グラフを {output_path} に保存しました。")
