import pandas as pd

# CSVファイルを読み込む
df = pd.read_csv('hijioriAmedas_data_utf8.csv', encoding='utf-8')

# 年月日をdatetime型に変換
df['年月日'] = pd.to_datetime(df['年月日'], errors='coerce')

# 欠損値を削除
df.dropna(subset=['年月日', '降水量の合計(mm)'], inplace=True)

# 1980年から2024年までのデータに絞る (今年を除外)
df = df[(df['年月日'].dt.year >= 1980) & (df['年月日'].dt.year < 2025)]

# 7月と8月のデータのみを抽出
df_july_august = df[df['年月日'].dt.month.isin([7, 8])]

# 年ごとに降水量を合計
yearly_precipitation = df_july_august.groupby(df_july_august['年月日'].dt.year)['降水量の合計(mm)'].sum().reset_index()

# 列名を修正
yearly_precipitation.rename(columns={'年月日': '年', '降水量の合計(mm)': '合計降水量(mm)'}, inplace=True)


# 最も降水量が多かった年トップ3
wettest_years = yearly_precipitation.sort_values(by='合計降水量(mm)', ascending=False).head(3)

# 最も降水量が少なかった年トップ3
driest_years = yearly_precipitation.sort_values(by='合計降水量(mm)', ascending=True).head(3)

print("7月・8月の合計降水量ランキング (1980年〜2024年)")
print("\n最も降水量が多かった年 トップ3:")
print(wettest_years.to_string(index=False))

print("\n最も降水量が少なかった年 トップ3:")
print(driest_years.to_string(index=False))