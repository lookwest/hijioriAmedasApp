
import pandas as pd
import datetime

try:
    # UTF-8でCSVファイルを読み込む
    df = pd.read_csv('hijioriAmedas_data_utf8.csv', encoding='utf-8')

    # 年月日をdatetime型に変換
    df['年月日'] = pd.to_datetime(df['年月日'], errors='coerce')

    # 最高気温を数値型に変換（変換できない値はNaNにする）
    df['最高気温(℃)'] = pd.to_numeric(df['最高気温(℃)'], errors='coerce')

    # 2025年8月のデータを抽出
    target_year = 2025
    target_month = 8
    
    # 年月がNaNでない行のみを対象にする
    df.dropna(subset=['年月日'], inplace=True)

    august_data = df[(df['年月日'].dt.year == target_year) & (df['年月日'].dt.month == target_month)]

    # 2025年8月の日付が存在するかチェック
    if august_data.empty:
        print(f"{target_year}年{target_month}月のデータが見つかりません。")
    else:
        # 最高気温が30℃以上の日（真夏日）をカウント
        hot_days_count = august_data[august_data['最高気温(℃)'] >= 30].shape[0]
        print(f"{target_year}年{target_month}月の真夏日の日数は {hot_days_count} 日です。")

except FileNotFoundError:
    print("エラー: hijioriAmedas_data_utf8.csv が見つかりません。")
except Exception as e:
    print(f"エラーが発生しました: {e}")
