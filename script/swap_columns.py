
import pandas as pd

file_path = 'hijioriAmedas_data_utf8.csv'

# CSVファイルを読み込む
df = pd.read_csv(file_path)

# 列のリストを取得
cols = df.columns.tolist()

# '最深積雪(cm)'と'降雪量合計(cm)'のインデックスを取得
snow_depth_index = cols.index('最深積雪(cm)')
snowfall_sum_index = cols.index('降雪量合計(cm)')

# 列名を入れ替える
cols[snow_depth_index], cols[snowfall_sum_index] = cols[snowfall_sum_index], cols[snow_depth_index]

# 新しい列順でDataFrameを再構築
df = df[cols]

# CSVファイルに上書き保存
df.to_csv(file_path, index=False, encoding='utf-8')

print(f"'{file_path}'の列の順番を更新しました。")
