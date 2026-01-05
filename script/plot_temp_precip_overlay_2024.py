
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates

def plot_temp_precip_overlay_2024():
    """
    2024年7月から9月の日別の最高気温と降水量を重ねてグラフにして保存する。
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
        data = df.loc[mask]

        if data.empty:
            print(f"{target_year}年7月〜9月のデータが見つかりません。")
            return

        # データを取得
        dates = data['年月日']
        max_temps = data['最高気温(℃)']
        precipitation = data['降水量の合計(mm)']

        # グラフの作成
        fig, ax1 = plt.subplots(figsize=(20, 8))

        # 1軸目（左）：最高気温を折れ線グラフでプロット
        color = 'tab:red'
        ax1.set_xlabel('日付')
        ax1.set_ylabel('最高気温 (℃)', color=color)
        line1 = ax1.plot(dates, max_temps, color=color, label='最高気温', marker='o', linestyle='-')
        ax1.tick_params(axis='y', labelcolor=color)

        # 2軸目（右）：降水量を棒グラフでプロット
        ax2 = ax1.twinx()
        color = 'tab:blue'
        ax2.set_ylabel('降水量 (mm)', color=color)
        bar1 = ax2.bar(dates, precipitation, color=color, alpha=0.6, label='降水量')
        ax2.tick_params(axis='y', labelcolor=color)

        # グラフのタイトルとX軸のフォーマット
        plt.title(f'{target_year}年7月〜9月の最高気温と降水量')
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        ax1.set_xticks(dates)
        ax1.tick_params(axis='x', rotation=90)

        # 凡例の表示
        lns = [line1[0], bar1]
        labs = [l.get_label() for l in lns]
        ax1.legend(lns, labs, loc='upper left')

        fig.tight_layout()

        # ファイルに保存
        output_filename = f'temp_precip_overlay_{target_year}.png'
        plt.savefig(output_filename)

        print(f"グラフを '{output_filename}' として保存しました。")

    except FileNotFoundError:
        print("エラー: hijioriAmedas_data_utf8.csv が見つかりません。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    plot_temp_precip_overlay_2024()
