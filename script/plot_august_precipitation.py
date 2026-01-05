
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib

# データの読み込み
try:
    df = pd.read_csv('hijioriAmedas_data_utf8.csv')
except FileNotFoundError:
    print("エラー: hijioriAmedas_data_utf8.csv が見つかりません。")
    exit()

# データの前処理
df['年月日'] = pd.to_datetime(df['年月日'])
df['降水量の合計(mm)'] = pd.to_numeric(df['降水量の合計(mm)'], errors='coerce')

# 1980年以降の8月のデータを抽出
df_august = df[(df['年月日'].dt.year >= 1980) & (df['年月日'].dt.month == 8)]

# 年ごとに合計降水量を計算
august_precip = df_august.groupby(df_august['年月日'].dt.year)['降水量の合計(mm)'].sum()

# グラフの作成
plt.figure(figsize=(15, 7))
august_precip.plot(kind='bar')

# グラフのタイトルとラベル
plt.title('1980年以降の8月の月間合計降水量')
plt.xlabel('年')
plt.ylabel('合計降水量 (mm)')
plt.xticks(rotation=45)
plt.tight_layout() # ラベルが重ならないように調整

# グラフをファイルに保存
output_filename = 'august_precipitation_since_1980.png'
plt.savefig(output_filename)

print(f"グラフを {output_filename} として保存しました。")
