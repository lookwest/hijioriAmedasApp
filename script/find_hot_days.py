
import pandas as pd

# CSVファイルを読み込む
df = pd.read_csv('hijioriAmedas_data.csv', header=None, names=['date', 'col2', 'col3', 'avg_temp', 'max_temp', 'min_temp', 'col7', 'col8', 'col9', 'col10', 'col11', 'col12'], encoding='cp932')

# 最高気温が30℃を超える日をフィルタリング
hot_days = df[df['max_temp'] > 30]

# 気温の高い順に並べ替え
hot_days_sorted = hot_days.sort_values(by='max_temp', ascending=False)

# 結果を新しいCSVファイルに出力
hot_days_sorted.to_csv('hot_days.csv', index=False)

print("最高気温が30℃を超えた日を抽出し、'hot_days.csv'に保存しました。")
