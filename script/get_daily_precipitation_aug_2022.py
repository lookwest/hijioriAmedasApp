
import pandas as pd

file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/hijioriAmedas_data.csv'

def get_daily_precipitation_aug_2022():
    """
    2022年8月の日ごとの降水量を抽出して出力します。
    """
    try:
        # Shift-JISでCSVを読み込む
        df = pd.read_csv(file_path, encoding='sjis', header=None, skiprows=1, on_bad_lines='skip')
        
        # カラム名を指定
        df.columns = [
            '日付', '降水量の合計(mm)', '1時間降水量の最大(mm)', 
            '平均気温(℃)', '最高気温(℃)', '最低気温(℃)', 
            '最大風速(m/s)', '最大風速の風向', '最大瞬間風速(m/s)', 
            '最大瞬間風速の風向', '最深積雪(cm)', '積雪深合計(cm)'
        ]

        # 日付をdatetimeオブジェクトに変換
        df['日付'] = pd.to_datetime(df['日付'], errors='coerce')
        df.dropna(subset=['日付'], inplace=True)

        # 降水量を数値に変換し、エラーはNaNとする
        df['降水量の合計(mm)'] = pd.to_numeric(df['降水量の合計(mm)'], errors='coerce')
        df.dropna(subset=['降水量の合計(mm)'], inplace=True)

        # 2022年8月のデータをフィルタリング
        aug_2022_data = df[(df['日付'].dt.year == 2022) & (df['日付'].dt.month == 8)].copy()

        if aug_2022_data.empty:
            print("2022年8月の降水データが見つかりませんでした。")
            return

        print("2022年8月の日ごとの降水量:")
        for index, row in aug_2022_data.iterrows():
            print(f"- {row['日付'].strftime('%Y/%m/%d')}: {row['降水量の合計(mm)']:.1f} mm")

    except FileNotFoundError:
        print(f"エラー: {file_path} が見つかりません。")
    except Exception as e:
        print(f"処理中にエラーが発生しました: {e}")

if __name__ == '__main__':
    get_daily_precipitation_aug_2022()
