import pandas as pd
import datetime

def list_september_avg_max_temp_last_10_years():
    """
    CSVファイルを読み込み、過去10年間の9月の平均最高気温を年ごとにリスト表示する。
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

        # 直近の年を取得
        latest_year = september_data['年月日'].dt.year.max()

        # 過去10年間をループ
        print("過去10年間の9月の平均最高気温:")
        for year in range(latest_year - 9, latest_year + 1):
            # 各年の9月のデータをフィルタリング
            yearly_september_data = september_data[september_data['年月日'].dt.year == year]

            if not yearly_september_data.empty:
                # 最高気温の平均を計算
                if '最高気温(℃)' in yearly_september_data.columns:
                    avg_max_temp = yearly_september_data['最高気温(℃)'].mean()
                    print(f"{year}年: {avg_max_temp:.2f}℃")
                else:
                    print(f"{year}年: エラー: '最高気温(℃)'列が見つかりません。")
            else:
                print(f"{year}年: データがありません。")

    except FileNotFoundError:
        print("エラー: hijioriAmedas_data_utf8.csv が見つかりません。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    list_september_avg_max_temp_last_10_years()