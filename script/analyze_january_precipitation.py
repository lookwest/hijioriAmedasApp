
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# データファイルを読み込む
file_path = 'hijioriAmedas_data_utf8.csv'
df = pd.read_csv(file_path, encoding='utf-8', na_values=['', ' ', '--', '×', '#'])

# '年月日'列をdatetime型に変換
df['年月日'] = pd.to_datetime(df['年月日'], errors='coerce')

# '降水量の合計(mm)'列を数値に変換し、NaNを0に置換
df['降水量の合計(mm)'] = pd.to_numeric(df['降水量の合計(mm)'], errors='coerce').fillna(0)

# 今日の日付を取得
today = datetime.now()

# 1月の開始日と終了日
january_start_day = 1
january_end_day = 31

# 今シーズンの1月の期間
this_january_start_date = datetime(today.year, 1, january_start_day)
this_january_end_date = datetime(today.year, 1, january_end_day)

# 昨シーズンの1月の期間
last_january_start_date = datetime(today.year - 1, 1, january_start_day)
last_january_end_date = datetime(today.year - 1, 1, january_end_day)

seasons_data = {
    "今シーズン": (this_january_start_date, this_january_end_date),
    "昨シーズン": (last_january_start_date, last_january_end_date)
}

plt.style.use('default')
plt.rcParams['font.sans-serif'] = ['Hiragino Sans']
plt.rcParams['axes.grid'] = True
fig, ax = plt.subplots(figsize=(12, 8))

colors = {"昨シーズン": "tab:blue", "今シーズン": "tab:red"}
markers = {"昨シーズン": "x", "今シーズン": "o"}
linestyles = {"昨シーズン": "--", "今シーズン": "-"}

# 各シーズンのデータを処理
final_cumulative_precipitation = {}
for season_name, (start_dt, end_dt) in seasons_data.items():
    mask = (df['年月日'] >= start_dt) & (df['年月日'] <= end_dt)
    season_df = df.loc[mask].copy()
    
    if not season_df.empty:
        season_df['累積降水量(mm)'] = season_df['降水量の合計(mm)'].cumsum()
        
        # 1月1日からの経過日数を計算
        season_df['経過日数'] = (season_df['年月日'] - datetime(start_dt.year, 1, 1)).dt.days
        
        ax.plot(season_df['経過日数'], season_df['累積降水量(mm)'], 
                marker=markers[season_name], linestyle=linestyles[season_name], 
                label=f'{season_name} ({start_dt.strftime("%Y/%m/%d")} - {end_dt.strftime("%Y/%m/%d")})', 
                color=colors[season_name])
        
        final_cumulative_precipitation[season_name] = season_df['累積降水量(mm)'].iloc[-1]

ax.set_xlabel('1月1日からの経過日数')
ax.set_ylabel('累積降水量 (mm)')
ax.set_title('昨シーズンと今シーズンの1月累積降水量比較')
ax.legend()
ax.set_xlim(left=0)

fig.tight_layout()
output_path = 'img/january_cumulative_precipitation_comparison.png'
plt.savefig(output_path)

print(f"グラフを {output_path} に保存しました。")

for season_name, total_precipitation in final_cumulative_precipitation.items():
    print(f"{season_name}の1月累積降水量: {total_precipitation:.1f} mm")
