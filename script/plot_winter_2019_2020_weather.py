import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# データファイルを読み込む
file_path = 'hijioriAmedas_data_utf8.csv'
df = pd.read_csv(file_path, encoding='utf-8')

# '年月日'をdatetime型に変換
df['年月日'] = pd.to_datetime(df['年月日'])

# 対象期間（2019年12月1日～2020年3月31日）のデータを抽出
start_date = '2019-12-01'
end_date = '2020-03-31'
mask = (df['年月日'] >= start_date) & (df['年月日'] <= end_date)
winter_df = df.loc[mask].copy()

#最深積雪(cm)の欠損値を0で埋める
winter_df['最深積雪(cm)'] = winter_df['最深積雪(cm)'].fillna(0)

# グラフ描画
fig, ax1 = plt.subplots(figsize=(15, 8))

# 1. 積雪深の推移
color = 'tab:blue'
ax1.set_xlabel('Date')
ax1.set_ylabel('Snow Depth (cm)', color=color)
ax1.plot(winter_df['年月日'], winter_df['最深積雪(cm)'], color=color, label='Snow Depth', zorder=2)
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(which='major', axis='y', linestyle='--', linewidth=0.5)

# 2. 降水量（棒グラフ）
ax2 = ax1.twinx()
color = 'tab:cyan'
ax2.set_ylabel('Daily Precipitation (mm)', color=color)
ax2.bar(winter_df['年月日'], winter_df['降水量の合計(mm)'], color=color, alpha=0.6, label='Precipitation', zorder=1)
ax2.tick_params(axis='y', labelcolor=color)

# 3. 最高・最低気温
ax3 = ax1.twinx()
ax3.spines['right'].set_position(('outward', 60))
ax3.set_ylabel('Temperature (°C)', color='tab:red')
ax3.plot(winter_df['年月日'], winter_df['最高気温(℃)'], color='tab:red', linestyle='-', label='Max Temp', linewidth=1.5, zorder=3)
ax3.plot(winter_df['年月日'], winter_df['最低気温(℃)'], color='tab:orange', linestyle='--', label='Min Temp', linewidth=1.5, zorder=3)
ax3.tick_params(axis='y', labelcolor='tab:red')
ax3.axhline(0, color='gray', linestyle=':', linewidth=1) # 0℃のライン

# グラフのフォーマット設定
fig.suptitle('Weather Trend in Winter 2019-2020 (Hijiori)', fontsize=16)
fig.legend(loc='upper right', bbox_to_anchor=(0.9, 0.9))
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.xticks(rotation=45)
fig.tight_layout(rect=[0, 0, 1, 0.96])

# グラフを保存
plt.savefig('winter_2019_2020_weather.png')

print("グラフ 'winter_2019_2020_weather.png' を生成しました。")
