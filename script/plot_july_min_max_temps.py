
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# macOSで利用可能な日本語フォントを設定
font_path = '/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc'  # 一般的なmacOSの日本語フォント
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/hijioriAmedas_data.csv'

try:
    # 日付(0)、最高気温(4)、最低気温(5)の列のみを読み込む
    df = pd.read_csv(file_path, encoding='shift_jis', header=0, usecols=[0, 4, 5],
                       names=['date', 'max_temp', 'min_temp'], na_values=['--', '', ' '])

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['max_temp'] = pd.to_numeric(df['max_temp'], errors='coerce')
    df['min_temp'] = pd.to_numeric(df['min_temp'], errors='coerce')

    # 2025年の7月のデータを抽出
    july_2025 = df[(df['date'].dt.year == 2025) & (df['date'].dt.month == 7)].copy()

    if july_2025.empty:
        print("エラー: 2025年7月のデータが見つかりませんでした。")
    else:
        july_2025['day'] = july_2025['date'].dt.day
        
        # グラフのセットアップ
        plt.figure(figsize=(16, 8))
        
        # バーの幅と位置を設定
        bar_width = 0.4
        index = np.arange(len(july_2025['day']))

        # 最高気温と最低気温の棒グラフを作成
        plt.bar(index - bar_width/2, july_2025['max_temp'], bar_width, label='最高気温')
        plt.bar(index + bar_width/2, july_2025['min_temp'], bar_width, label='最低気温')

        plt.title('2025年7月の日別 最高・最低気温', fontproperties=font_prop, fontsize=16)
        plt.xlabel('日', fontproperties=font_prop, fontsize=12)
        plt.ylabel('気温 (°C)', fontproperties=font_prop, fontsize=12)
        plt.xticks(index, july_2025['day'])
        plt.legend(prop=font_prop)
        plt.grid(True, axis='y')
        plt.tight_layout()

        output_filename = 'july_2025_min_max_temp_bar.png'
        plt.savefig(output_filename)
        print(f"グラフを '{output_filename}' として保存しました。")

except FileNotFoundError:
    print(f"エラー: ファイルが見つかりません - {file_path}")
except Exception as e:
    print(f"スクリプトの実行中にエラーが発生しました: {e}")
