
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/hijioriAmedas_data.csv'
output_image_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/hot_days_by_month.png'

def plot_hot_days():
    """
    最高気温が30℃を超えた日数を月別に集計し、積み上げグラフを作成して保存します。
    """
    try:
        # Shift-JISでCSVを読み込む
        df = pd.read_csv(file_path, encoding='sjis', header=None, skiprows=1, on_bad_lines='skip')
        
        # カラム名を指定
        df.columns = [
            '日付', '降水量の合計(mm)', '1時間降水量の最大(mm)', 
            '平均気温(℃)', '最高気温(℃)', '最低気温(℃)', 
            '最大風速(m/s)', '最大風速の風向', '最大瞬間風速(m/s)', 
            '最大瞬間風速の風向', '最深積雪(cm)', '積雪深合計(cm)'
        ]

        # 日付と最高気温の列を抽出
        df_filtered = df[['日付', '最高気温(℃)']].copy()

        # 日付をdatetimeオブジェクトに変換
        df_filtered['日付'] = pd.to_datetime(df_filtered['日付'], errors='coerce')
        
        # 無効な日付を削除
        df_filtered.dropna(subset=['日付'], inplace=True)

        # 最高気温を数値に変換し、エラーはNaNとする
        df_filtered['最高気温(℃)'] = pd.to_numeric(df_filtered['最高気温(℃)'], errors='coerce')
        
        # NaNの行を削除
        df_filtered.dropna(subset=['最高気温(℃)'], inplace=True)

        # 年と月を抽出 (df_filtered全体に対して)
        df_filtered['年'] = df_filtered['日付'].dt.year
        df_filtered['月'] = df_filtered['日付'].dt.month

        # 5月から10月のデータのみを対象とする
        df_filtered = df_filtered[df_filtered['月'].isin(range(5, 11))]

        # 30℃を超えた日をマーク
        df_filtered['is_hot_day'] = (df_filtered['最高気温(℃)'] > 30).astype(int)

        # 年と月でグループ化し、is_hot_dayの合計をカウント
        # これにより、30℃を超えた日がない月も0として含まれる
        hot_days_count = df_filtered.groupby(['年', '月'])['is_hot_day'].sum().unstack(fill_value=0)

        # hot_days_countが空の場合の処理（データが全くない場合）
        if hot_days_count.empty:
            print("データに最高気温が30℃を超えた日が全くありませんでした。空のグラフを生成します。")

        # グラフの作成
        fig, ax = plt.subplots(figsize=(12, 7))
        hot_days_count.plot(kind='bar', stacked=True, ax=ax, cmap='tab10')

        ax.set_title('Number of Days with Max Temperature > 30°C by Month per Year')
        ax.set_xlabel('Year')
        ax.set_ylabel('Number of Days > 30°C')
        ax.legend(title='Month', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        # 画像として保存
        plt.savefig(output_image_path)
        print(f"グラフが {output_image_path} に保存されました。")

    except FileNotFoundError:
        print(f"エラー: {file_path} が見つかりません。")
    except Exception as e:
        print(f"処理中にエラーが発生しました: {e}")

if __name__ == '__main__':
    plot_hot_days()
