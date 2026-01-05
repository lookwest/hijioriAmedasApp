
import pandas as pd

# データの読み込み
try:
    df = pd.read_csv('hijioriAmedas_data_utf8.csv')
except FileNotFoundError:
    print("エラー: hijioriAmedas_data_utf8.csv が見つかりません。")
    exit()

# 年月日をdatetime型に変換
df['年月日'] = pd.to_datetime(df['年月日'])

# 降水量の列を数値型に変換（変換できない値はNaNにする）
df['降水量の合計(mm)'] = pd.to_numeric(df['降水量の合計(mm)'], errors='coerce')

# 2025年のデータを抽出
df_2025 = df[df['年月日'].dt.year == 2025].copy()

if df_2025.empty:
    print("2025年のデータはまだありません。")
else:
    # 2025年の最大降水量を求める
    max_precip_row = df_2025.loc[df_2025['降水量の合計(mm)'].idxmax()]
    
    # 日付を YYYY/MM/DD 形式の文字列に変換
    date_str = max_precip_row['年月日'].strftime('%Y年%m月%d日')
    max_precip = max_precip_row['降水量の合計(mm)']
    
    print(f"2025年の最大降水量は {date_str} の {max_precip}mm です。")
