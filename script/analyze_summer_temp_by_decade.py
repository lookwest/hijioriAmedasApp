
import pandas as pd

file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/hijioriAmedas_data.csv'

def analyze_summer_temp_by_decade():
    """
    夏の平均気温を10年ごとに分析します。
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

        # 日付と平均気温の列を抽出
        df_temp = df[['日付', '平均気温(℃)']].copy()

        # 日付をdatetimeオブジェクトに変換
        df_temp['日付'] = pd.to_datetime(df_temp['日付'], errors='coerce')
        df_temp.dropna(subset=['日付'], inplace=True)

        # 平均気温を数値に変換し、エラーはNaNとする
        df_temp['平均気温(℃)'] = pd.to_numeric(df_temp['平均気温(℃)'], errors='coerce')
        df_temp.dropna(subset=['平均気温(℃)'], inplace=True)

        # 夏の月 (6, 7, 8月) をフィルタリング
        df_summer = df_temp[df_temp['日付'].dt.month.isin([6, 7, 8])].copy()

        # 年代を計算
        def get_decade(year):
            if 1980 <= year <= 1989:
                return '1980s'
            elif 1990 <= year <= 1999:
                return '1990s'
            elif 2000 <= year <= 2009:
                return '2000s'
            elif 2010 <= year <= 2019:
                return '2010s'
            elif 2020 <= year:
                return '2020s'
            else:
                return 'Other'

        df_summer['Decade'] = df_summer['日付'].dt.year.apply(get_decade)

        # 各年代の夏の平均気温を計算
        summer_avg_temps = df_summer.groupby('Decade')['平均気温(℃)'].mean().reindex(['1980s', '1990s', '2000s', '2010s', '2020s'])

        print("各年代の夏の平均気温:")
        for decade, avg_temp in summer_avg_temps.items():
            if pd.notna(avg_temp):
                print(f"- {decade}: {avg_temp:.2f} °C")
            else:
                print(f"- {decade}: データなし")

    except FileNotFoundError:
        print(f"エラー: {file_path} が見つかりません。")
    except Exception as e:
        print(f"処理中にエラーが発生しました: {e}")

if __name__ == '__main__':
    analyze_summer_temp_by_decade()
