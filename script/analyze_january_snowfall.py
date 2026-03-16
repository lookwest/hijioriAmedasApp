
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# データファイルを読み込む
file_path = 'hijioriAmedas_data_utf8.csv'
df = pd.read_csv(file_path, encoding='utf-8', na_values=['', ' ', '--', '×', '#'])

# '年月日'列をdatetime型に変換
df['年月日'] = pd.to_datetime(df['年月日'], errors='coerce')

# '降雪量合計(cm)'列を数値に変換し、NaNを0に置換
df['降雪量合計(cm)'] = pd.to_numeric(df['降雪量合計(cm)'], errors='coerce').fillna(0)

# 今日の日付を取得 (今回は1月のみの比較なので、今日の日付は直接使用しない)
# today = datetime.now()

# 1月の開始日と終了日
january_start_day = 1
january_end_day = 31

# 今シーズンの1月の期間
this_january_start_date = datetime(datetime.now().year, 1, january_start_day)
this_january_end_date = datetime(datetime.now().year, 1, january_end_day)

# 昨シーズンの1月の期間
last_january_start_date = datetime(datetime.now().year - 1, 1, january_start_day)
last_january_end_date = datetime(datetime.now().year - 1, 1, january_end_day)

seasons_data = {
    "今シーズン": (this_january_start_date, this_january_end_date),
    "昨シーズン": (last_january_start_date, last_january_end_date)
}

plt.style.use('default')
plt.rcParams['font.sans-serif'] = ['Hiragino Sans']
plt.rcParams['axes.grid'] = True

fig, ax = plt.subplots(figsize=(12, 8))

# 各シーズンのデータを処理
final_cumulative_snowfall = {}
for season_name, (start_dt, end_dt) in seasons_data.items():
    mask = (df['年月日'] >= start_dt) & (df['年月日'] <= end_dt)
    season_df = df.loc[mask].copy()
    
    if not season_df.empty:
        season_df['累積降雪量(cm)'] = season_df['降雪量合計(cm)'].cumsum()
        
        # 1月1日からの経過日数を計算
        season_df['経過日数'] = (season_df['年月日'] - datetime(start_dt.year, 1, 1)).dt.days
        
        ax.plot(season_df['経過日数'], season_df['累積降雪量(cm)'], 
                marker='o' if season_name == "今シーズン" else 'x', 
                linestyle='-' if season_name == "今シーズン" else '--', 
                label=f'{season_name} ({start_dt.strftime("%Y/%m/%d")} - {end_dt.strftime("%Y/%m/%d")})', 
                color='tab:red' if season_name == "今シーズン" else 'tab:blue')
        
        final_cumulative_snowfall[season_name] = season_df['累積降雪量(cm)'].iloc[-1]

ax.set_xlabel('1月1日からの経過日数')
ax.set_ylabel('累積降雪量 (cm)')
ax.set_title('昨シーズンと今シーズンの1月累積降雪量比較')
ax.legend()
ax.set_xlim(left=0)

# X軸の範囲を調整 (1月の最大日数に合わせる)
max_elapsed_days = january_end_day - january_start_day
ax.set_xlim(0, max_elapsed_days + 1) # X軸の範囲を1月1日からの経過日数で設定
ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True)) # X軸の目盛りを整数にする

fig.tight_layout()
output_path = 'img/january_cumulative_snowfall_comparison.png'
plt.savefig(output_path)

print(f"グラフを {output_path} に保存しました。")

for season_name, total_snowfall in final_cumulative_snowfall.items():
    print(f"{season_name}の1月累積降雪量: {total_snowfall:.1f} cm")
