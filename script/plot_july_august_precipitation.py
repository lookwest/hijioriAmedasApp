
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib

# CSVファイルを読み込む
df = pd.read_csv('hijioriAmedas_data_utf8.csv', encoding='utf-8')

# 年月日をdatetime型に変換
df['年月日'] = pd.to_datetime(df['年月日'], errors='coerce')

# 欠損値を削除
df.dropna(subset=['年月日', '降水量の合計(mm)'], inplace=True)

# 1980年以降のデータに絞る
df = df[df['年月日'].dt.year >= 1980]

# 7月と8月のデータのみを抽出
df_july_august = df[df['年月日'].dt.month.isin([7, 8])]

# 年ごとに降水量を合計
yearly_precipitation = df_july_august.groupby(df_july_august['年月日'].dt.year)['降水量の合計(mm)'].sum()

# グラフを作成
plt.figure(figsize=(15, 7))
plt.bar(yearly_precipitation.index, yearly_precipitation.values)
plt.title('肘折 7月・8月 合計降水量 (1980年〜現在)')
plt.xlabel('年')
plt.ylabel('合計降水量 (mm)')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# グラフを保存
plt.savefig('july_august_precipitation_1980-2025.png')

plt.close()

print("グラフ 'july_august_precipitation_1980-2025.png' を作成しました。")
