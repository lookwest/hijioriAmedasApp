
import pandas as pd
import matplotlib.pyplot as plt

file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/hijioriAmedas_data.csv'
output_image_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/winter_snow_depth_2006_2007.png'

def plot_winter_snow_depth():
    """
    2006年から2007年にかけての12月から2月末までの日ごとの最大積雪深をグラフ化します。
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

        # 日付と最深積雪、最高気温の列を抽出
        df_combined = df[['日付', '最深積雪(cm)', '最高気温(℃)']].copy()

        # 日付をdatetimeオブジェクトに変換
        df_combined['日付'] = pd.to_datetime(df_combined['日付'], errors='coerce')
        df_combined.dropna(subset=['日付'], inplace=True)

        # 最深積雪と最高気温を数値に変換し、エラーはNaNとする
        df_combined['最深積雪(cm)'] = pd.to_numeric(df_combined['最深積雪(cm)'], errors='coerce')
        df_combined['最高気温(℃)'] = pd.to_numeric(df_combined['最高気温(℃)'], errors='coerce')
        
        # NaNの行を削除（両方のデータが存在する行のみを対象）
        df_combined.dropna(subset=['最深積雪(cm)', '最高気温(℃)'], inplace=True)

        # 2006年12月1日から2007年2月28日までのデータをフィルタリング
        start_date = pd.to_datetime('2006/12/01')
        end_date = pd.to_datetime('2007/02/28')
        winter_data = df_combined[(df_combined['日付'] >= start_date) & (df_combined['日付'] <= end_date)].copy()

        if winter_data.empty:
            print("指定された期間のデータが見つかりませんでした。")
            return

        # 日付でソート
        winter_data.sort_values(by='日付', inplace=True)

        # グラフの作成
        fig, ax1 = plt.subplots(figsize=(15, 7))

        # 積雪深のプロット (左Y軸)
        ax1.plot(winter_data['日付'], winter_data['最深積雪(cm)'], marker='o', linestyle='-', color='blue', label='Maximum Snow Depth')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Maximum Snow Depth (cm)', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')
        ax1.grid(True)

        # 最高気温のプロット (右Y軸)
        ax2 = ax1.twinx()
        ax2.plot(winter_data['日付'], winter_data['最高気温(℃)'], marker='x', linestyle='--', color='red', label='Maximum Temperature')
        ax2.set_ylabel('Maximum Temperature (°C)', color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        # タイトルと凡例
        plt.title('Daily Maximum Snow Depth and Temperature (Dec 2006 - Feb 2007)')
        fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))
        plt.xticks(rotation=45)
        plt.tight_layout()

        # 画像として保存
        plt.savefig(output_image_path)
        print(f"グラフが {output_image_path} に保存されました。")

    except FileNotFoundError:
        print(f"エラー: {file_path} が見つかりません。")
    except Exception as e:
        print(f"処理中にエラーが発生しました: {e}")

if __name__ == '__main__':
    plot_winter_snow_depth()
