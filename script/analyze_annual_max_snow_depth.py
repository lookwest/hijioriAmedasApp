import pandas as pd

# データファイルを読み込む
file_path = 'hijioriAmedas_data_utf8.csv'
try:
    df = pd.read_csv(file_path, encoding='utf-8')

    # '年月日'をdatetime型に変換
    df['年月日'] = pd.to_datetime(df['年月日'])

    # 数値に変換できないデータをNaNにし、列の型を数値に変換
    snow_col = '最深積雪(cm)'
    df[snow_col] = pd.to_numeric(df[snow_col], errors='coerce')

    # 年を抽出
    df['年'] = df['年月日'].dt.year

    # 年ごとの最大積雪深を計算
    annual_max_snow = df.groupby('年')[snow_col].max()

    # 結果を降順でソート
    top_snow_years = annual_max_snow.sort_values(ascending=False)

    # 結果を表示
    print("年別最大積雪深ランキング (トップ10):")
    print(top_snow_years.head(10))

except FileNotFoundError:
    print(f"エラー: {file_path} が見つかりません。")
except Exception as e:
    print(f"処理中にエラーが発生しました: {e}")
