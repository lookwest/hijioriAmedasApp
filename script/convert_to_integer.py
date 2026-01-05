
import pandas as pd
import numpy as np

file_path = 'hijioriAmedas_data_utf8.csv'

# CSVファイルを読み込む
df = pd.read_csv(file_path)

# 対象列
columns_to_convert = ['降雪量合計(cm)', '最深積雪(cm)']

for col in columns_to_convert:
    if col in df.columns:
        # 欠損値を0で埋めてから整数型に変換
        # pandasのInt64Dtype() を使用するとNaNを許容する整数型に変換できるが、
        # 今回は「値を整数にする」という明確な指示のため、NaNを0で埋める
        df[col] = df[col].fillna(0).astype(int)
    else:
        print(f"警告: 列 '{col}' がファイルに見つかりませんでした。")

# CSVファイルに上書き保存
df.to_csv(file_path, index=False, encoding='utf-8')

print(f"'{file_path}'の'{columns_to_convert}'列を整数に変換しました。")
