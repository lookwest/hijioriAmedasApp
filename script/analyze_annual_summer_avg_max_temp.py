
import pandas as pd

file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/hijioriAmedas_data.csv'

def analyze_annual_summer_avg_max_temp():
    """
    毎年の夏の最高気温の平均を分析します。
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
        df_temp = df[['日付', '最高気温(℃)']].copy()

        # 日付をdatetimeオブジェクトに変換
        df_temp['日付'] = pd.to_datetime(df_temp['日付'], errors='coerce')
        df_temp.dropna(subset=['日付'], inplace=True)

        # 最高気温を数値に変換し、エラーはNaNとする
        df_temp['最高気温(℃)'] = pd.to_numeric(df_temp['最高気温(℃)'], errors='coerce')
        df_temp.dropna(subset=['最高気温(℃)'], inplace=True)

        # 夏の月 (6, 7, 8月) をフィルタリング
        df_summer = df_temp[df_temp['日付'].dt.month.isin([6, 7, 8])].copy()

        # 年を抽出
        df_summer['Year'] = df_summer['日付'].dt.year

        # 各年の夏の最高気温の平均を計算
        annual_summer_avg_max_temps = df_summer.groupby('Year')['最高気温(℃)'].mean()

        print("毎年の夏の最高気温の平均:")
        for year, avg_max_temp in annual_summer_avg_max_temps.items():
            if pd.notna(avg_max_temp):
                print(f"- {year}年: {avg_max_temp:.2f} °C")
            else:
                print(f"- {year}年: データなし")

    except FileNotFoundError:
        print(f"エラー: {file_path} が見つかりません。")
    except Exception as e:
        print(f"処理中にエラーが発生しました: {e}")

if __name__ == '__main__':
    analyze_annual_summer_avg_max_temp()
