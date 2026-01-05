
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

def plot_august_2023_max_temp():
    """
    CSVファイルを読み込み、2023年8月の日別の最高気温をグラフにして保存する。
    """
    try:
        # MatplotlibのバックエンドをAggに設定
        mpl.use('Agg')

        # 日本語フォントの設定
        plt.rcParams['font.sans-serif'] = ['Hiragino Sans']
        plt.rcParams['axes.unicode_minus'] = False

        # CSVファイルを読み込む
        df = pd.read_csv('hijioriAmedas_data_utf8.csv', encoding='utf-8')

        # '年月日'列をdatetimeオブジェクトに変換
        df['年月日'] = pd.to_datetime(df['年月日'])

        # 2023年8月のデータをフィルタリング
        target_year = 2023
        target_month = 8
        august_2023_data = df[(df['年月日'].dt.year == target_year) & (df['年月日'].dt.month == target_month)]

        if august_2023_data.empty:
            print(f"{target_year}年{target_month}月のデータが見つかりません。")
            return

        # 日ごとのデータを取得
        days = august_2023_data['年月日'].dt.day
        max_temps = august_2023_data['最高気温(℃)']

        # グラフの作成
        plt.figure(figsize=(12, 6))
        plt.plot(days, max_temps, marker='o', linestyle='-', color='r')

        # タイトルとラベルの設定
        plt.title(f'{target_year}年{target_month}月の日別最高気温')
        plt.xlabel('日')
        plt.ylabel('最高気温 (℃)')
        plt.grid(True)
        plt.xticks(days, rotation=45)
        plt.tight_layout()

        # ファイルに保存
        output_filename = f'august_{target_year}_max_temp.png'
        plt.savefig(output_filename)

        print(f"グラフを '{output_filename}' として保存しました。")

    except FileNotFoundError:
        print("エラー: hijioriAmedas_data_utf8.csv が見つかりません。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    plot_august_2023_max_temp()
