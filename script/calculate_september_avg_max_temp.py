import pandas as pd

def calculate_september_avg_max_temp():
    """
    CSVファイルを読み込み、9月の平均最高気温を計算して出力する。
    """
    try:
        # CSVファイルをUTF-8エンコーディングで読み込む
        df = pd.read_csv('hijioriAmedas_data_utf8.csv', encoding='utf-8')

        # '年月日'列をdatetimeオブジェクトに変換
        df['年月日'] = pd.to_datetime(df['年月日'])

        # 9月のデータをフィルタリング
        september_data = df[df['年月日'].dt.month == 9]

        if september_data.empty:
            print("9月のデータはまだありません。")
            return

        # 最高気温の平均を計算
        # 列名'最高気温(℃)'が正しいことを確認
        if '最高気温(℃)' in september_data.columns:
            avg_max_temp = september_data['最高気温(℃)'].mean()
            print(f"9月の平均最高気温は: {avg_max_temp:.2f}℃")
        else:
            print("エラー: '最高気温(℃)'列が見つかりません。")

    except FileNotFoundError:
        print("エラー: hijioriAmedas_data_utf8.csv が見つかりません。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    calculate_september_avg_max_temp()