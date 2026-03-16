import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# データファイルを読み込む
file_path = 'hijioriAmedas_data_utf8.csv'
df = pd.read_csv(file_path, encoding='utf-8', na_values=['', ' ', '--', '×', '#'])

# '年月日'列をdatetime型に変換
df['年月日'] = pd.to_datetime(df['年月日'], errors='coerce')

# 必要な列を数値に変換し、NaNを0に置換
columns_to_numeric = ['降水量の合計(mm)', '降雪量合計(cm)', '最深積雪(cm)']
for col in columns_to_numeric:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# --- データ期間の設定 ---
# データセット内の最新の日付を取得
latest_date = df['年月日'].max()

# 今シーズン
current_season_start = datetime(latest_date.year - (1 if latest_date.month < 12 else 0), 12, 1)
current_season_end = latest_date
# 昨シーズン
last_season_start = datetime(current_season_start.year - 1, 12, 1)
last_season_end = datetime(current_season_end.year - 1, current_season_end.month, current_season_end.day)

# --- データフレームの準備 ---
def prepare_season_data(df, start_date, end_date):
    mask = (df['年月日'] >= start_date) & (df['年月日'] <= end_date)
    season_df = df.loc[mask].copy()
    season_df['経過日数'] = (season_df['年月日'] - start_date).dt.days
    season_df['累積降水量(mm)'] = season_df['降水量の合計(mm)'].cumsum()
    season_df['累積降雪量(cm)'] = season_df['降雪量合計(cm)'].cumsum()
    return season_df

df_current_season = prepare_season_data(df, current_season_start, current_season_end)
df_last_season = prepare_season_data(df, last_season_start, last_season_end)

# --- 平年値の計算 ---
normal_year_end_year = current_season_start.year -1
normal_year_start_year = normal_year_end_year - 29

normal_dfs = []
for year in range(normal_year_start_year, normal_year_end_year + 1):
    start = datetime(year, 12, 1)
    end = datetime(year + 1, current_season_end.month, current_season_end.day)
    
    # 期間内のデータを抽出
    mask = (df['年月日'] >= start) & (df['年月日'] <= end)
    temp_df = df.loc[mask].copy()
    
    if not temp_df.empty:
        temp_df['経過日数'] = (temp_df['年月日'] - start).dt.days
        # 今シーズンの日数を超えるデータは除外
        temp_df = temp_df[temp_df['経過日数'] < len(df_current_season)]
        normal_dfs.append(temp_df)

if normal_dfs:
    df_normal = pd.concat(normal_dfs)
    normal_values = df_normal.groupby('経過日数')[['降水量の合計(mm)', '降雪量合計(cm)', '最深積雪(cm)']].mean()
    normal_values['累積降水量(mm)'] = normal_values['降水量の合計(mm)'].cumsum()
    normal_values['累積降雪量(cm)'] = normal_values['降雪量合計(cm)'].cumsum()
else:
    normal_values = pd.DataFrame()


# --- グラフ描画 ---
plt.style.use('default')
plt.rcParams['font.sans-serif'] = ['Hiragino Sans']
plt.rcParams['axes.grid'] = True

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 18), sharex=True)
fig.suptitle(f'気象データ比較 (12/1〜{current_season_end.month}/{current_season_end.day})', fontsize=16)

# --- 1. 累積降水量 ---
ax1.plot(df_current_season['経過日数'], df_current_season['累積降水量(mm)'], marker='o', linestyle='-', label=f'今シーズン ({current_season_start.year}-{current_season_end.year})', color='tab:red', zorder=5)
ax1.plot(df_last_season['経過日数'], df_last_season['累積降水量(mm)'], marker='x', linestyle='--', label=f'昨シーズン ({last_season_start.year}-{last_season_end.year})', color='tab:blue', zorder=4)
if not normal_values.empty:
    ax1.plot(normal_values.index, normal_values['累積降水量(mm)'], linestyle=':', label=f'平年値 ({normal_year_start_year}-{normal_year_end_year})', color='green')
ax1.set_ylabel('累積降水量 (mm)')
ax1.set_title('累積降水量')
ax1.legend()

# --- 2. 累積降雪量 ---
ax2.plot(df_current_season['経過日数'], df_current_season['累積降雪量(cm)'], marker='o', linestyle='-', label=f'今シーズン ({current_season_start.year}-{current_season_end.year})', color='tab:red', zorder=5)
ax2.plot(df_last_season['経過日数'], df_last_season['累積降雪量(cm)'], marker='x', linestyle='--', label=f'昨シーズン ({last_season_start.year}-{last_season_end.year})', color='tab:blue', zorder=4)
if not normal_values.empty:
    ax2.plot(normal_values.index, normal_values['累積降雪量(cm)'], linestyle=':', label=f'平年値 ({normal_year_start_year}-{normal_year_end_year})', color='green')
ax2.set_ylabel('累積降雪量 (cm)')
ax2.set_title('累積降雪量')
ax2.legend()

# --- 3. 積雪深 ---
ax3.plot(df_current_season['経過日数'], df_current_season['最深積雪(cm)'], marker='o', linestyle='-', label=f'今シーズン ({current_season_start.year}-{current_season_end.year})', color='tab:red', zorder=5)
ax3.plot(df_last_season['経過日数'], df_last_season['最深積雪(cm)'], marker='x', linestyle='--', label=f'昨シーズン ({last_season_start.year}-{last_season_end.year})', color='tab:blue', zorder=4)
if not normal_values.empty:
    ax3.plot(normal_values.index, normal_values['最深積雪(cm)'], linestyle=':', label=f'平年値 ({normal_year_start_year}-{normal_year_end_year})', color='green')
ax3.set_xlabel('12月1日からの経過日数')
ax3.set_ylabel('最深積雪 (cm)')
ax3.set_title('最深積雪')
ax3.legend()


# X軸の調整
max_days = max(len(df_current_season), len(df_last_season))
ax3.set_xlim(0, max_days -1)
ax3.xaxis.set_major_locator(plt.MaxNLocator(integer=True, nbins=15))

fig.tight_layout(rect=[0, 0.03, 1, 0.97])
output_path = 'img/seasonal_weather_comparison.png'
plt.savefig(output_path)

print(f"グラフを {output_path} に保存しました。")
