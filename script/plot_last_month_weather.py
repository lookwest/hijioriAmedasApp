
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# データファイルを読み込む
file_path = 'hijioriAmedas_data_utf8.csv'
df = pd.read_csv(file_path, encoding='utf-8', na_values=['', ' ', '--', '×', '#'])

# '年月日'列をdatetime型に変換
df['年月日'] = pd.to_datetime(df['年月日'], errors='coerce')

# 必要な列のデータ型を数値に変換
for col in ['最高気温(℃)', '最低気温(℃)', '最深積雪(cm)']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 直近1ヶ月の期間を定義
end_date = df['年月日'].max()
if pd.isna(end_date):
    end_date = datetime.now()
start_date = end_date - timedelta(days=31)

# データをフィルタリング
mask = (df['年月日'] >= start_date) & (df['年月日'] <= end_date)
df_last_month = df.loc[mask].copy()

# グラフ描画
plt.style.use('default')
plt.rcParams['font.sans-serif'] = ['Hiragino Sans']
plt.rcParams['axes.grid'] = True

fig, ax1 = plt.subplots(figsize=(12, 8))

# 気温のグラフ (左Y軸)
ax1.plot(df_last_month['年月日'], df_last_month['最高気温(℃)'], marker='o', linestyle='-', label='最高気温', color='tab:red')
ax1.plot(df_last_month['年月日'], df_last_month['最低気温(℃)'], marker='o', linestyle='-', label='最低気温', color='tab:blue')
ax1.set_xlabel('日付')
ax1.set_ylabel('気温 (℃)', color='black')
ax1.set_ylim(-10, 15) # 気温のY軸範囲を設定
ax1.tick_params(axis='y', labelcolor='black')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
ax1.tick_params(axis='x', rotation=45)


# 積雪深のグラフ (右Y軸)
ax2 = ax1.twinx()
ax2.bar(df_last_month['年月日'], df_last_month['最深積雪(cm)'], label='最深積雪', color='lightblue', alpha=0.7)
ax2.set_ylabel('最深積雪 (cm)', color='tab:blue')
ax2.tick_params(axis='y', labelcolor='tab:blue')
ax2.set_ylim(0, 250) # 積雪のY軸範囲を設定

# 凡例
lines, labels = ax1.get_legend_handles_labels()
bars, bar_labels = ax2.get_legend_handles_labels()
ax2.legend(lines + bars, labels + bar_labels, loc='upper left')

# タイトル
plt.title(f'直近1ヶ月の気象データ ({start_date.strftime("%Y/%m/%d")} - {end_date.strftime("%Y/%m/%d")})')

# レイアウト調整と保存
fig.tight_layout()
output_path = 'img/last_month_weather.png'
plt.savefig(output_path)

print(f"グラフを {output_path} に保存しました。")
