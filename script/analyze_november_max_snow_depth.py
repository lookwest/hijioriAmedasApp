
import pandas as pd

file_path = 'hijioriAmedas_data_utf8.csv'

# CSVファイルを読み込む
try:
    df = pd.read_csv(file_path, encoding='utf-8')
except FileNotFoundError:
    print(f"エラー: ファイル '{file_path}' が見つかりません。")
    exit()

# '年月日'列をdatetime型に変換
df['年月日'] = pd.to_datetime(df['年月日'], errors='coerce')

# 変換できなかった行を削除
df = df.dropna(subset=['年月日'])

# 11月のデータを抽出
november_data = df[df['年月日'].dt.month == 11]

# '最深積雪(cm)'列が存在するか確認
if '最深積雪(cm)' not in november_data.columns:
    print("エラー: '最深積雪(cm)'列が見つかりません。")
    exit()

# 年ごとにグループ化し、各年の最深積雪の最大値とその日付を取得
results = []
for year, group in november_data.groupby(november_data['年月日'].dt.year):
    if not group.empty:
        max_snow_row = group.loc[group['最深積雪(cm)'].idxmax()]
        results.append({
            '年': year,
            '日付': max_snow_row['年月日'].strftime('%Y/%m/%d'),
            '最大積雪深(cm)': max_snow_row['最深積雪(cm)']
        })

# 結果をDataFrameに変換して出力
results_df = pd.DataFrame(results)
print("年ごとの11月の最大積雪深と記録日:")
print(results_df)
