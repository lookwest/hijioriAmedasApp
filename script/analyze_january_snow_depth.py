
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

# シーズンのデータを抽出する関数
def get_season_data_january(df, start_date, end_date):
    mask = (df['年月日'] >= start_date) & (df['年月日'] <= end_date)
    season_df = df.loc[mask].copy()
    season_df['経過日数'] = (season_df['年月日'] - datetime(start_date.year, 1, 1)).dt.days
    return season_df

# 今シーズンのデータ (1月)
df_this_january = get_season_data_january(df, this_january_start_date, this_january_end_date)
# 昨シーズンのデータ (1月)
df_last_january = get_season_data_january(df, last_january_start_date, last_january_end_date)

# 平年値の計算 (過去30年、1月のみ)
current_year = datetime.now().year
average_start_year = current_year - 30

all_january_data = []
for year in range(average_start_year, current_year):
    january_start = datetime(year, 1, 1)
    january_end = datetime(year, 1, 31)
    
    january_mask = (df['年月日'] >= january_start) & (df['年月日'] <= january_end)
    january_df = df.loc[january_mask].copy()
    
    if not january_df.empty:
        january_df['経過日数'] = (january_df['年月日'] - january_start).dt.days
        all_january_data.append(january_df)

if all_january_data:
    df_all_past_januaries = pd.concat(all_january_data)
    average_snow_depth_january = df_all_past_januaries.groupby('経過日数')['最深積雪(cm)'].mean().reset_index()
else:
    average_snow_depth_january = pd.DataFrame(columns=['経過日数', '最深積雪(cm)'])


# グラフ描画
plt.style.use('default')
plt.rcParams['font.sans-serif'] = ['Hiragino Sans']
plt.rcParams['axes.grid'] = True

fig, ax = plt.subplots(figsize=(12, 8))

# 今シーズンの1月最深積雪
if not df_this_january.empty:
    ax.plot(df_this_january['経過日数'], df_this_january['最深積雪(cm)'], marker='o', linestyle='-', label=f'今シーズン ({this_january_start_date.strftime("%Y/%m/%d")} - {this_january_end_date.strftime("%Y/%m/%d")})', color='tab:red')

# 昨シーズンの1月最深積雪
if not df_last_january.empty:
    ax.plot(df_last_january['経過日数'], df_last_january['最深積雪(cm)'], marker='x', linestyle='--', label=f'昨シーズン ({last_january_start_date.strftime("%Y/%m/%d")} - {last_january_end_date.strftime("%Y/%m/%d")})', color='tab:blue')

# 平年値 (1月)
if not average_snow_depth_january.empty:
    ax.plot(average_snow_depth_january['経過日数'], average_snow_depth_january['最深積雪(cm)'], linestyle='-.', label=f'平年値 ({average_start_year}~{current_year-1}年平均)', color='tab:green')


ax.set_xlabel('1月1日からの経過日数')
ax.set_ylabel('最深積雪 (cm)')
ax.set_title('今シーズン、昨シーズン、平年値の1月最深積雪比較')
ax.legend()

# X軸の範囲を調整 (1月の最大日数に合わせる)
max_elapsed_days_january = january_end_day - january_start_day
ax.set_xlim(0, max_elapsed_days_january + 1)
ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True)) # X軸の目盛りを整数にする

fig.tight_layout()
output_path = 'img/january_seasonal_snow_depth_comparison.png'
plt.savefig(output_path)

print(f"グラフを {output_path} に保存しました。")

# 数値データの出力
print("\n--- 1月最深積雪データ分析 ---")

if not df_this_january.empty:
    max_snow_this_january = df_this_january['最深積雪(cm)'].max()
    date_max_snow_this_january = df_this_january.loc[df_this_january['最深積雪(cm)'].idxmax()]['年月日'].strftime('%Y-%m-%d')
    current_snow_this_january = df_this_january['最深積雪(cm)'].iloc[-1]
    print(f"今シーズン1月:")
    print(f"  最大最深積雪量: {max_snow_this_january:.1f} cm (観測日: {date_max_snow_this_january})")
    print(f"  1月末の最深積雪量: {current_snow_this_january:.1f} cm")
else:
    print(f"今シーズン1月: データなし")

if not df_last_january.empty:
    max_snow_last_january = df_last_january['最深積雪(cm)'].max()
    date_max_snow_last_january = df_last_january.loc[df_last_january['最深積雪(cm)'].idxmax()]['年月日'].strftime('%Y-%m-%d')
    current_snow_last_january = df_last_january['最深積雪(cm)'].iloc[-1]
    print(f"昨シーズン1月:")
    print(f"  最大最深積雪量: {max_snow_last_january:.1f} cm (観測日: {date_max_snow_last_january})")
    print(f"  1月末の最深積雪量: {current_snow_last_january:.1f} cm")
else:
    print(f"昨シーズン1月: データなし")

if not average_snow_depth_january.empty:
    # 1月末の経過日数に対応する平年値を探す
    january_elapsed_day_end = january_end_day - january_start_day
    if january_elapsed_day_end in average_snow_depth_january['経過日数'].values:
        average_january_snow_end = average_snow_depth_january[average_snow_depth_january['経過日数'] == january_elapsed_day_end]['最深積雪(cm)'].iloc[0]
        print(f"平年値 (1996~{current_year-1}年平均、1月末): {average_january_snow_end:.1f} cm")
    else:
        print(f"平年値 (1996~{current_year-1}年平均、1月末): データなし (1月末の経過日数に該当する平年値が存在しません)")
else:
    print(f"平年値: データなし")
