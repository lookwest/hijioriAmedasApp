
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

def plot_september_2024_precipitation():
    """
    CSVファイルを読み込み、2024年9月の日別の降水量をグラフにして保存する。
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

        # 2024年9月のデータをフィルタリング
        target_year = 2024
        target_month = 9
        september_2024_data = df[(df['年月日'].dt.year == target_year) & (df['年月日'].dt.month == target_month)]

        if september_2024_data.empty:
            print(f"{target_year}年{target_month}月のデータが見つかりません。")
            return

        # 日ごとのデータを取得
        days = september_2024_data['年月日'].dt.day
        # 降水量の列名を特定（ファイルによって異なる可能性を考慮）
        precipitation_col = '降水量の合計(mm)'
        if precipitation_col not in df.columns:
            print(f"エラー: 列 '{precipitation_col}' が見つかりません。")
            return
        precipitation = september_2024_data[precipitation_col]

        # グラフの作成 (棒グラフ)
        plt.figure(figsize=(12, 6))
        plt.bar(days, precipitation, color='skyblue')

        # タイトルとラベルの設定
        plt.title(f'{target_year}年{target_month}月の日別降水量')
        plt.xlabel('日')
        plt.ylabel('降水量 (mm)')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.xticks(days, rotation=45)
        plt.tight_layout()

        # ファイルに保存
        output_filename = f'september_{target_year}_precipitation.png'
        plt.savefig(output_filename)

        print(f"グラフを '{output_filename}' として保存しました。")

    except FileNotFoundError:
        print("エラー: hijioriAmedas_data_utf8.csv が見つかりません。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    plot_september_2024_precipitation()
