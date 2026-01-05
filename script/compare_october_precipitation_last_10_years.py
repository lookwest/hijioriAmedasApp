
import pandas as pd

# データの読み込み
try:
    df = pd.read_csv('hijioriAmedas_data_utf8.csv', encoding='utf-8')
except FileNotFoundError:
    print("ファイル 'hijioriAmedas_data_utf8.csv' が見つかりません。")
    exit()

# 列名
date_col = '年月日'
precip_col = '降水量の合計(mm)'

# 日付列をdatetime型に変換
df[date_col] = pd.to_datetime(df[date_col])

# 2016年から2025年までの範囲を決定
start_year = 2016
end_year = 2025

print(f"{start_year}年から{end_year}年までの10月の合計降水量:")
print()

# 各年についてループ
for year in range(start_year, end_year + 1):
    # その年の10月のデータを抽出
    df_oct = df[(df[date_col].dt.year == year) & (df[date_col].dt.month == 10)]

    if not df_oct.empty:
        # 合計降水量を計算
        total_precip = df_oct[precip_col].sum()

        # 結果の表示
        print(f"{year}年10月: {total_precip:.1f} mm")
    else:
        print(f"{year}年10月: データがありません")
