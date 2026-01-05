
import pandas as pd

file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/hijioriAmedas_data.csv'

def analyze_wind_direction_by_season():
    """
    CSVファイルから季節ごとの風向きの傾向を分析します。
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

        # 日付と風向きの列を抽出
        df_wind = df[['日付', '最大風速の風向']].copy()

        # 日付をdatetimeオブジェクトに変換
        df_wind['日付'] = pd.to_datetime(df_wind['日付'], errors='coerce')
        df_wind.dropna(subset=['日付'], inplace=True)

        # 月を抽出
        df_wind['月'] = df_wind['日付'].dt.month

        # 季節を定義
        def get_season(month):
            if month in [3, 4, 5]:
                return 'Spring'
            elif month in [6, 7, 8]:
                return 'Summer'
            elif month in [9, 10, 11]:
                return 'Autumn'
            else: # 12, 1, 2
                return 'Winter'
        
        df_wind['Season'] = df_wind['月'].apply(get_season)

        # 風向きの傾向を分析
        print("季節ごとの風向きの傾向:")
        for season in ['Spring', 'Summer', 'Autumn', 'Winter']:
            season_data = df_wind[df_wind['Season'] == season]
            if not season_data.empty:
                # 空白や無効な風向きデータを削除
                valid_wind_directions = season_data['最大風速の風向'].dropna()
                valid_wind_directions = valid_wind_directions[valid_wind_directions != '-']
                valid_wind_directions = valid_wind_directions[valid_wind_directions != '']

                if not valid_wind_directions.empty:
                    wind_direction_counts = valid_wind_directions.value_counts()
                    most_common_wind = wind_direction_counts.index[0]
                    print(f"- {season}: 最も多い風向きは {most_common_wind} ({wind_direction_counts.iloc[0]} 回)")
                else:
                    print(f"- {season}: 有効な風向きデータがありませんでした。")
            else:
                print(f"- {season}: データがありませんでした。")

    except FileNotFoundError:
        print(f"エラー: {file_path} が見つかりません。")
    except Exception as e:
        print(f"処理中にエラーが発生しました: {e}")

if __name__ == '__main__':
    analyze_wind_direction_by_season()
