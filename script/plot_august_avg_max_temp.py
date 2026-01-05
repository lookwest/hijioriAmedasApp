
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

def plot_august_avg_max_temp():
    """
    CSVファイルを読み込み、1978年からの各年8月の平均最高気温をグラフにして保存する。
    """
    try:
        # MatplotlibのバックエンドをAggに設定
        mpl.use('Agg')

        # 日本語フォントの設定
        # macOSの一般的なフォントを指定
        plt.rcParams['font.sans-serif'] = ['Hiragino Sans']
        plt.rcParams['axes.unicode_minus'] = False

        # CSVファイルを読み込む
        df = pd.read_csv('hijioriAmedas_data_utf8.csv', encoding='utf-8')

        # '年月日'列をdatetimeオブジェクトに変換
        df['年月日'] = pd.to_datetime(df['年月日'])

        # 8月のデータのみをフィルタリング
        august_data = df[df['年月日'].dt.month == 8]
        august_data = august_data[august_data['年月日'].dt.year >= 1978]

        # 年ごとにグループ化し、最高気温の平均を計算
        yearly_avg_max_temp = august_data.groupby(august_data['年月日'].dt.year)['最高気温(℃)'].mean()

        # グラフの作成
        plt.figure(figsize=(15, 7))
        plt.plot(yearly_avg_max_temp.index, yearly_avg_max_temp.values, marker='o', linestyle='-')

        # タイトルとラベルの設定
        plt.title('肘折AMeDAS: 1978年からの8月の年別平均最高気温')
        plt.xlabel('年')
        plt.ylabel('平均最高気温 (℃)')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # ファイルに保存
        output_filename = 'august_avg_max_temp_by_year.png'
        plt.savefig(output_filename)

        print(f"グラフを '{output_filename}' として保存しました。")

    except FileNotFoundError:
        print("エラー: hijioriAmedas_data_utf8.csv が見つかりません。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    plot_august_avg_max_temp()
