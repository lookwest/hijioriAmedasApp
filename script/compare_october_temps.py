import pandas as pd

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

# 2024年と2025年の10月のデータを抽出
df_2024_oct = df[(df[date_col].dt.year == 2024) & (df[date_col].dt.month == 10)]
df_2025_oct = df[(df[date_col].dt.year == 2025) & (df[date_col].dt.month == 10)]

# 2024年10月の平均気温を計算
avg_max_temp_2024 = df_2024_oct[max_temp_col].mean()
avg_min_temp_2024 = df_2024_oct[min_temp_col].mean()

# 2025年10月の平均気温を計算
avg_max_temp_2025 = df_2025_oct[max_temp_col].mean()
avg_min_temp_2025 = df_2025_oct[min_temp_col].mean()

# 結果の表示
print("2024年10月:")
if pd.notna(avg_max_temp_2024):
    print(f"  平均最高気温: {avg_max_temp_2024:.2f} ℃")
else:
    print("  平均最高気温: データがありません")
if pd.notna(avg_min_temp_2024):
    print(f"  平均最低気温: {avg_min_temp_2024:.2f} ℃")
else:
    print("  平均最低気温: データがありません")


print("\n2025年10月:")
if pd.notna(avg_max_temp_2025):
    print(f"  平均最高気温: {avg_max_temp_2025:.2f} ℃")
else:
    print("  平均最高気温: データがありません")
if pd.notna(avg_min_temp_2025):
    print(f"  平均最低気温: {avg_min_temp_2025:.2f} ℃")
else:
    print("  平均最低気温: データがありません")
