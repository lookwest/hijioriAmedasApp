
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates

def plot_september_2025_weather():
    """
    2025年9月の日別の最高気温、最低気温と降水量を重ねてグラフにして保存する。
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

        # 2025年9月のデータをフィルタリング
        target_year = 2025
        target_month = 9
        start_date = f'{target_year}-{target_month:02d}-01'
        end_date = f'{target_year}-{target_month:02d}-30'
        mask = (df['年月日'] >= start_date) & (df['年月日'] <= end_date)
        data = df.loc[mask]

        if data.empty:
            print(f"{target_year}年{target_month}月のデータが見つかりません。")
            return

        # データを取得
        dates = data['年月日']
        max_temps = data['最高気温(℃)']
        min_temps = data['最低気温(℃)']
        precipitation = data['降水量の合計(mm)']

        # グラフの作成
        fig, ax1 = plt.subplots(figsize=(20, 8))

        # 1軸目（左）：最高気温と最低気温を折れ線グラフでプロット
        color_max = 'tab:red'
        color_min = 'tab:orange'
        ax1.set_xlabel('日付')
        ax1.set_ylabel('気温 (℃)')
        line1 = ax1.plot(dates, max_temps, color=color_max, label='最高気温', marker='o', linestyle='-')
        line2 = ax1.plot(dates, min_temps, color=color_min, label='最低気温', marker='^', linestyle='--')
        ax1.tick_params(axis='y')

        # 2軸目（右）：降水量を棒グラフでプロット
        ax2 = ax1.twinx()
        color_precip = 'tab:blue'
        ax2.set_ylabel('降水量 (mm)', color=color_precip)
        bar1 = ax2.bar(dates, precipitation, color=color_precip, alpha=0.6, label='降水量')
        ax2.tick_params(axis='y', labelcolor=color_precip)

        # グラフのタイトルとX軸のフォーマット
        plt.title(f'{target_year}年{target_month}月の最高・最低気温と降水量')
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        ax1.set_xticks(dates)
        ax1.tick_params(axis='x', rotation=90)

        # 凡例の表示
        lns = [line1[0], line2[0], bar1]
        labs = [l.get_label() for l in lns]
        ax1.legend(lns, labs, loc='upper left')

        fig.tight_layout()

        # ファイルに保存
        output_filename = f'september_{target_year}_weather.png'
        plt.savefig(output_filename)

        print(f"グラフを '{output_filename}' として保存しました。")

    except FileNotFoundError:
        print("エラー: hijioriAmedas_data_utf8.csv が見つかりません。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    plot_september_2025_weather()
