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
today = datetime.now()
this_year_end_date = today
this_year_start_date = datetime(today.year, 12, 1) if today.month >= 12 else datetime(today.year - 1, 12, 1)
mask_this_year = (df['年月日'] >= this_year_start_date) & (df['年月日'] <= this_year_end_date)
df_this_year = df.loc[mask_this_year].copy()
df_this_year['累積降雪量(cm)'] = df_this_year['降雪量合計(cm)'].cumsum()
df_this_year['経過日数'] = (df_this_year['年月日'] - datetime(this_year_start_date.year, 12, 1)).dt.days

# 昨年の期間 (12/1 - 1/4)
last_year_end_date = datetime(today.year - 1, today.month, today.day)
last_year_start_date = datetime(today.year - 1, 12, 1) if today.month >= 12 else datetime(today.year - 2, 12, 1)
mask_last_year = (df['年月日'] >= last_year_start_date) & (df['年月日'] <= last_year_end_date)
df_last_year = df.loc[mask_last_year].copy()
df_last_year['累積降雪量(cm)'] = df_last_year['降雪量合計(cm)'].cumsum()
df_last_year['経過日数'] = (df_last_year['年月日'] - datetime(last_year_start_date.year, 12, 1)).dt.days

# グラフ描画
plt.style.use('default')
plt.rcParams['font.sans-serif'] = ['Hiragino Sans']
plt.rcParams['axes.grid'] = True

fig, ax = plt.subplots(figsize=(12, 8))

# 今年の累積降雪量
ax.plot(df_this_year['経過日数'], df_this_year['累積降雪量(cm)'], marker='o', linestyle='-', label=f'今シーズン ({this_year_start_date.strftime("%Y/%m/%d")} - {this_year_end_date.strftime("%Y/%m/%d")})', color='tab:red')

# 昨年の累積降雪量
ax.plot(df_last_year['経過日数'], df_last_year['累積降雪量(cm)'], marker='x', linestyle='--', label=f'昨シーズン ({last_year_start_date.strftime("%Y/%m/%d")} - {last_year_end_date.strftime("%Y/%m/%d")})', color='tab:blue')


ax.set_xlabel('12月1日からの経過日数')
ax.set_ylabel('累積降雪量 (cm)')
ax.set_title('今シーズンと昨シーズンの累積降雪量比較')
ax.legend()
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
# ax.tick_params(axis='x', rotation=45)

# Y軸の範囲を調整 (最大累積値の少し上まで)
max_cumulative_snow = max(df_this_year['累積降雪量(cm)'].max(), df_last_year['累積降雪量(cm)'].max())
ax.set_ylim(0, max_cumulative_snow * 1.1)
max_elapsed_days = max(df_this_year['経過日数'].max(), df_last_year['経過日数'].max())
ax.set_xlim(0, max_elapsed_days + 5) # X軸の範囲を12月1日からの経過日数で設定
ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True)) # X軸の目盛りを整数にする


fig.tight_layout()
output_path = 'img/cumulative_snowfall_comparison.png'
plt.savefig(output_path)

print(f"グラフを {output_path} に保存しました。")

if not df_this_year.empty:
    print(f"今シーズンの最終累積降雪量: {df_this_year['累積降雪量(cm)'].iloc[-1]:.1f} cm")
if not df_last_year.empty:
    print(f"昨シーズンの最終累積降雪量: {df_last_year['累積降雪量(cm)'].iloc[-1]:.1f} cm")