
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# macOSで利用可能な日本語フォントを設定
font_path = '/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc'  # 一般的なmacOSの日本語フォント
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/hijioriAmedas_data.csv'

try:
    # 日付(0)と最高気温(4)の列のみを読み込む
    df = pd.read_csv(file_path, encoding='shift_jis', header=0, usecols=[0, 4],
                       names=['date', 'max_temp'], na_values=['--', '', ' '])

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['max_temp'] = pd.to_numeric(df['max_temp'], errors='coerce')

    # 2024年と2025年の7月のデータを抽出
    july_2024 = df[(df['date'].dt.year == 2024) & (df['date'].dt.month == 7)].copy()
    july_2025 = df[(df['date'].dt.year == 2025) & (df['date'].dt.month == 7)].copy()

    if july_2024.empty or july_2025.empty:
        if july_2024.empty:
            print("エラー: 2024年7月のデータが見つかりませんでした。")
        if july_2025.empty:
            print("エラー: 2025年7月のデータが見つかりませんでした。")
    else:
        july_2024['day'] = july_2024['date'].dt.day
        july_2025['day'] = july_2025['date'].dt.day

        plt.figure(figsize=(14, 7))
        plt.plot(july_2024['day'], july_2024['max_temp'], marker='o', linestyle='-', label='2024年')
        plt.plot(july_2025['day'], july_2025['max_temp'], marker='x', linestyle='--', label='2025年')

        plt.title('2024年と2025年の7月の日別最高気温比較', fontproperties=font_prop, fontsize=16)
        plt.xlabel('日', fontproperties=font_prop, fontsize=12)
        plt.ylabel('最高気温 (°C)', fontproperties=font_prop, fontsize=12)
        plt.xticks(range(1, 32))
        plt.legend(prop=font_prop)
        plt.grid(True)
        plt.tight_layout()

        output_filename = 'july_max_temp_comparison_2024_2025.png'
        plt.savefig(output_filename)
        print(f"グラフを '{output_filename}' として保存しました。")

except FileNotFoundError:
    print(f"エラー: ファイルが見つかりません - {file_path}")
except Exception as e:
    print(f"スクリプトの実行中にエラーが発生しました: {e}")
