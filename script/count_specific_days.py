import pandas as pd
import matplotlib.pyplot as plt

# 日本語フォントの設定
plt.rcParams['font.family'] = 'Hiragino Sans'

# CSVファイルを読み込む
df = pd.read_csv(
    'hijioriAmedas_data.csv',
    header=None,
    encoding='cp932',
    names=[
        '日付', '降水量の合計(mm)', '1時間降水量の最大(mm)', 
        '平均気温(℃)', '最高気温(℃)', '最低気温(℃)', 
        '最大風速(m/s)', '最大風速の風向', '最大瞬間風速(m/s)', 
        '最大瞬間風速の風向', '最深積雪(cm)', '積雪深合計(cm)'
    ]
)

# データ型を数値に変換（エラーはNaNに）
for col in ['降水量の合計(mm)', '最深積雪(cm)', '最低気温(℃)', '最高気温(℃)']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 日付をdatetimeオブジェクトに変換
df['日付'] = pd.to_datetime(df['日付'], errors='coerce')

# 条件に合う日をフィルタリング
specific_days = df[
    (df['降水量の合計(mm)'] == 0) &
    (df['最深積雪(cm)'] == 0) &
    (df['最低気温(℃)'] >= 10) &
    (df['最高気温(℃)'] <= 25)
].copy()

# 年を抽出
specific_days['年'] = specific_days['日付'].dt.year

# 年ごとに日数をカウント
yearly_counts = specific_days['年'].value_counts().sort_index()

# グラフを作成
plt.figure(figsize=(12, 6))
yearly_counts.plot(kind='bar')
plt.title('条件に合う日の年別の日数')
plt.xlabel('年')
plt.ylabel('日数')
plt.xticks(rotation=45)
plt.tight_layout()

# グラフを画像として保存
plt.savefig('specific_days_per_year.png')

print("グラフを 'specific_days_per_year.png' に保存しました。")