import pandas as pd
from datetime import datetime

# データの読み込み
try:
    df = pd.read_csv('hijioriAmedas_data_utf8.csv', encoding='utf-8')
except FileNotFoundError:
    print("ファイル 'hijioriAmedas_data_utf8.csv' が見つかりません。")
    exit()

# 列名
date_col = '年月日'
max_temp_col = '最高気温(℃)'
min_temp_col = '最低気温(℃)'

# 日付列をdatetime型に変換
df[date_col] = pd.to_datetime(df[date_col])

# 現在の年から過去10年間の範囲を決定
# Note: 2025年11月7日のため、current_yearは2025年
current_year = 2025
start_year = current_year - 9

print(f"{start_year}年から{current_year}年までの10月の気温比較:")

# 各年についてループ
for year in range(start_year, current_year + 1):
    # その年の10月のデータを抽出
    df_oct = df[(df[date_col].dt.year == year) & (df[date_col].dt.month == 10)]

    print() # 年の区切りに改行を入れる

    if not df_oct.empty:
        # 平均気温を計算
        avg_max_temp = df_oct[max_temp_col].mean()
        avg_min_temp = df_oct[min_temp_col].mean()

        # 結果の表示
        print(f"{year}年10月:")
        if pd.notna(avg_max_temp):
            print(f"  平均最高気温: {avg_max_temp:.2f} ℃")
        else:
            print("  平均最高気温: データがありません")
        if pd.notna(avg_min_temp):
            print(f"  平均最低気温: {avg_min_temp:.2f} ℃")
        else:
            print("  平均最低気温: データがありません")
    else:
        print(f"{year}年10月: データがありません")