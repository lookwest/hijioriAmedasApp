
import pandas as pd

def list_august_avg_max_temp_by_year():
    """
    CSVファイルを読み込み、1978年からの各年8月の平均最高気温を計算して出力する。
    """
    try:
        # CSVファイルをUTF-8エンコーディングで読み込む
        df = pd.read_csv('hijioriAmedas_data_utf8.csv', encoding='utf-8')

        # '年月日'列をdatetimeオブジェクトに変換
        df['年月日'] = pd.to_datetime(df['年月日'])

        # 8月のデータのみをフィルタリング
        august_data = df[df['年月日'].dt.month == 8]

        # 1978年以降のデータに絞り込む
        august_data = august_data[august_data['年月日'].dt.year >= 1978]

        # 年ごとにグループ化し、最高気温の平均を計算
        yearly_avg_max_temp = august_data.groupby(august_data['年月日'].dt.year)['最高気温(℃)'].mean()

        print("1978年からの各年8月の平均最高気温:")
        for year, avg_temp in yearly_avg_max_temp.items():
            print(f"{year}年: {avg_temp:.2f}℃")

    except FileNotFoundError:
        print("エラー: hijioriAmedas_data_utf8.csv が見つかりません。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    list_august_avg_max_temp_by_year()
