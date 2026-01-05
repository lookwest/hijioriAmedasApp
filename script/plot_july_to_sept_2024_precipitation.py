
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates

def plot_july_to_sept_2024_precipitation():
    """
    CSVファイルを読み込み、2024年7月から9月の日別の降水量をグラフにして保存する。
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

        # 2024年7月から9月のデータをフィルタリング
        target_year = 2024
        start_date = f'{target_year}-07-01'
        end_date = f'{target_year}-09-30'
        mask = (df['年月日'] >= start_date) & (df['年月日'] <= end_date)
        july_to_sept_data = df.loc[mask]

        if july_to_sept_data.empty:
            print(f"{target_year}年7月〜9月のデータが見つかりません。")
            return

        # 日ごとのデータを取得
        dates = july_to_sept_data['年月日']
        precipitation = july_to_sept_data['降水量の合計(mm)']

        # グラフの作成 (棒グラフ)
        plt.figure(figsize=(20, 8))
        plt.bar(dates, precipitation, color='royalblue', width=0.8)

        # タイトルとラベルの設定
        plt.title(f'{target_year}年7月〜9月の日別降水量')
        plt.xlabel('日付')
        plt.ylabel('降水量 (mm)')
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # X軸のフォーマットを設定
        ax = plt.gca()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        # データの日にちに合わせて目盛りを表示
        ax.set_xticks(dates)
        plt.xticks(rotation=90, ha='center')
        plt.tight_layout()

        # ファイルに保存
        output_filename = f'july_to_sept_{target_year}_precipitation.png'
        plt.savefig(output_filename)

        print(f"グラフを '{output_filename}' として保存しました。")

    except FileNotFoundError:
        print("エラー: hijioriAmedas_data_utf8.csv が見つかりません。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    plot_july_to_sept_2024_precipitation()
