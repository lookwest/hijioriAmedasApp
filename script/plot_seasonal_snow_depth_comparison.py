import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# データファイルを読み込む
file_path = 'hijioriAmedas_data_utf8.csv'
df = pd.read_csv(file_path, encoding='utf-8', na_values=['', ' ', '--', '×', '#'])

# '年月日'列をdatetime型に変換
df['年月日'] = pd.to_datetime(df['年月日'], errors='coerce')

# '最深積雪(cm)'列を数値に変換し、NaNを0に置換
df['最深積雪(cm)'] = pd.to_numeric(df['最深積雪(cm)'], errors='coerce').fillna(0)

# 今日の日付を取得
today = datetime.now()

# 今シーズンの期間 (12月1日から本日まで)
this_season_start_year = today.year if today.month >= 12 else today.year - 1
this_season_start_date = datetime(this_season_start_year, 12, 1)
this_season_end_date = today

# 昨シーズンの期間 (前年の12月1日から今年の本日と同じ日付まで)
last_season_start_year = this_season_start_year - 1
last_season_start_date = datetime(last_season_start_year, 12, 1)
last_season_end_date = datetime(today.year - 1, today.month, today.day)

# シーズンのデータを抽出する関数
def get_season_data(df, start_date, end_date):
    mask = (df['年月日'] >= start_date) & (df['年月日'] <= end_date)
    season_df = df.loc[mask].copy()
    season_df['経過日数'] = (season_df['年月日'] - datetime(start_date.year, 12, 1)).dt.days
    return season_df

# 今シーズンのデータ
df_this_season = get_season_data(df, this_season_start_date, this_season_end_date)
max_elapsed_days_this_season = df_this_season['経過日数'].max() if not df_this_season.empty else 0
# 昨シーズンのデータ
df_last_season = get_season_data(df, last_season_start_date, last_season_end_date)

# 平年値の計算 (過去30年)
current_year = today.year
average_start_year = current_year - 30

all_winter_data = []
for year in range(average_start_year, current_year):
    # 各年の冬のシーズン (12月1日から翌年5月31日までとする)
    winter_start = datetime(year, 12, 1)
    winter_end = datetime(year + 1, 5, 31) # 翌年5月末まで
    
    winter_mask = (df['年月日'] >= winter_start) & (df['年月日'] <= winter_end)
    winter_df = df.loc[winter_mask].copy()
    
    if not winter_df.empty:
        winter_df['経過日数'] = (winter_df['年月日'] - winter_start).dt.days
        all_winter_data.append(winter_df)

if all_winter_data:
    df_all_past_winters = pd.concat(all_winter_data)
    average_snow_depth = df_all_past_winters.groupby('経過日数')['最深積雪(cm)'].mean().reset_index()
else:
    average_snow_depth = pd.DataFrame(columns=['経過日数', '最深積雪(cm)'])


# グラフ描画
plt.style.use('default')
plt.rcParams['font.sans-serif'] = ['Hiragino Sans']
plt.rcParams['axes.grid'] = True

fig, ax = plt.subplots(figsize=(12, 8))

# 今シーズンの最深積雪
if not df_this_season.empty:
    ax.plot(df_this_season['経過日数'], df_this_season['最深積雪(cm)'], marker='o', linestyle='-', label=f'今シーズン ({this_season_start_date.strftime("%Y/%m/%d")} - {this_season_end_date.strftime("%Y/%m/%d")})', color='tab:red')

# 昨シーズンの最深積雪
if not df_last_season.empty:
    ax.plot(df_last_season['経過日数'], df_last_season['最深積雪(cm)'], marker='x', linestyle='--', label=f'昨シーズン ({last_season_start_date.strftime("%Y/%m/%d")} - {last_season_end_date.strftime("%Y/%m/%d")})', color='tab:blue')

# 平年値
if not average_snow_depth.empty:
    ax.plot(average_snow_depth['経過日数'], average_snow_depth['最深積雪(cm)'], linestyle='-.', label=f'平年値 ({average_start_year}~{current_year-1}年平均)', color='tab:green')


ax.set_xlabel('12月1日からの経過日数')
ax.set_ylabel('最深積雪 (cm)')
ax.set_title('今シーズン、昨シーズン、平年値の最深積雪比較')
ax.legend()

# X軸の範囲を調整 (最大経過日数に合わせる)
max_elapsed_days = max_elapsed_days_this_season
ax.set_xlim(0, max_elapsed_days + 5) 
ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True)) # X軸の目盛りを整数にする

fig.tight_layout()
output_path = 'img/seasonal_snow_depth_comparison.png'
plt.savefig(output_path)

print(f"グラフを {output_path} に保存しました。")

# 数値データの出力
print("\n--- 最深積雪データ分析 ---")

if not df_this_season.empty:
    max_snow_this_season = df_this_season['最深積雪(cm)'].max()
    date_max_snow_this_season = df_this_season.loc[df_this_season['最深積雪(cm)'].idxmax()]['年月日'].strftime('%Y-%m-%d')
    current_snow_this_season = df_this_season['最深積雪(cm)'].iloc[-1]
    print(f"今シーズン ({this_season_end_date.strftime('%Y/%m/%d')}時点):")
    print(f"  最大最深積雪量: {max_snow_this_season:.1f} cm (観測日: {date_max_snow_this_season})")
    print(f"  現在の最深積雪量: {current_snow_this_season:.1f} cm")
else:
    print(f"今シーズン ({this_season_end_date.strftime('%Y/%m/%d')}時点): データなし")

if not df_last_season.empty:
    max_snow_last_season = df_last_season['最深積雪(cm)'].max()
    date_max_snow_last_season = df_last_season.loc[df_last_season['最深積雪(cm)'].idxmax()]['年月日'].strftime('%Y-%m-%d')
    current_snow_last_season = df_last_season['最深積雪(cm)'].iloc[-1]
    print(f"昨シーズン ({last_season_end_date.strftime('%Y/%m/%d')}時点):")
    print(f"  最大最深積雪量: {max_snow_last_season:.1f} cm (観測日: {date_max_snow_last_season})")
    print(f"  現在の最深積雪量: {current_snow_last_season:.1f} cm")
else:
    print(f"昨シーズン ({last_season_end_date.strftime('%Y/%m/%d')}時点): データなし")

if not average_snow_depth.empty:
    # 現在の経過日数を計算
    # todayが12月1日以降の場合、todayの年の12月1日を基準
    # todayが12月1日より前の場合、前年の12月1日を基準
    if today.month >= 12:
        base_date_for_elapsed_day = datetime(today.year, 12, 1)
    else:
        base_date_for_elapsed_day = datetime(today.year - 1, 12, 1)
    current_elapsed_day = (today - base_date_for_elapsed_day).days
    
    # current_elapsed_day が average_snow_depth の '経過日数' に存在する場合
    if current_elapsed_day in average_snow_depth['経過日数'].values:
        average_current_snow = average_snow_depth[average_snow_depth['経過日数'] == current_elapsed_day]['最深積雪(cm)'].iloc[0]
        print(f"平年値 ({average_start_year}~{current_year-1}年平均、本日時点): {average_current_snow:.1f} cm")
    else:
        print(f"平年値 ({average_start_year}~{current_year-1}年平均、本日時点): データなし (現在の経過日数に該当する平年値が存在しません)")
else:
    print(f"平年値: データなし")

