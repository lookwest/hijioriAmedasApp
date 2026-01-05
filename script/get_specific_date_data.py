import pandas as pd
import sys

def get_specific_date_data(year, month, day):
    """
    指定された年月日の気象データを表示する。
    """
    try:
        # CSVファイルを読み込む
        df = pd.read_csv('hijioriAmedas_data_utf8.csv', encoding='utf-8')

        # '年月日'列をdatetimeオブジェクトに変換
        df['年月日'] = pd.to_datetime(df['年月日'])

        # 指定された年月日でデータを検索
        target_date = pd.to_datetime(f"{year}-{month}-{day}")
        date_data = df[df['年月日'] == target_date]

        if not date_data.empty:
            print(f"{year}年{month}月{day}のデータ:")
            # データを整形して表示（インデックスなし）
            print(date_data.to_string(index=False))
        else:
            print(f"{year}年{month}月{day}のデータは見つかりませんでした。")

    except FileNotFoundError:
        print("エラー: hijioriAmedas_data_utf8.csv が見つかりません。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    if len(sys.argv) == 4:
        try:
            year = int(sys.argv[1])
            month = int(sys.argv[2])
            day = int(sys.argv[3])
            get_specific_date_data(year, month, day)
        except ValueError:
            print("年、月、日は整数で指定してください。例: python get_specific_date_data.py 2023 8 12")
    else:
        # 引数がない場合は、ユーザーの要求通り2023年8月12日のデータを表示
        get_specific_date_data(2023, 8, 12)