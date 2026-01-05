
import pandas as pd
from datetime import timedelta

file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/hijioriAmedas_data.csv'

def analyze_dry_spell_and_heavy_rain(dry_spell_threshold_days=7, heavy_rain_threshold_mm=50):
    """
    乾燥期間の後に大雨が降る傾向があるかを分析します。
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

        # 日付と降水量の列を抽出
        df_rain = df[['日付', '降水量の合計(mm)']].copy()

        # 日付をdatetimeオブジェクトに変換
        df_rain['日付'] = pd.to_datetime(df_rain['日付'], errors='coerce')
        df_rain.dropna(subset=['日付'], inplace=True)

        # 降水量を数値に変換し、エラーは0とする（欠損値は降水量0とみなす）
        df_rain['降水量の合計(mm)'] = pd.to_numeric(df_rain['降水量の合計(mm)'], errors='coerce').fillna(0)

        # 日付でソート
        df_rain.sort_values(by='日付', inplace=True)
        df_rain.reset_index(drop=True, inplace=True)

        dry_spell_ends_followed_by_heavy_rain = 0
        total_dry_spell_ends = 0

        current_dry_streak = 0
        for i in range(len(df_rain)):
            if df_rain.loc[i, '降水量の合計(mm)'] == 0:
                current_dry_streak += 1
            else:
                # 乾燥期間が終了したとき
                if current_dry_streak >= dry_spell_threshold_days:
                    total_dry_spell_ends += 1
                    # 乾燥期間の次の日が大雨かどうかをチェック
                    if df_rain.loc[i, '降水量の合計(mm)'] >= heavy_rain_threshold_mm:
                        dry_spell_ends_followed_by_heavy_rain += 1
                current_dry_streak = 0
        
        print(f"分析期間: {df_rain['日付'].min().strftime('%Y/%m/%d')} から {df_rain['日付'].max().strftime('%Y/%m/%d')}")
        print(f"乾燥期間の定義: 降水量0mmが {dry_spell_threshold_days} 日以上連続")
        print(f"大雨の定義: 1日の降水量が {heavy_rain_threshold_mm}mm 以上")
        print(f"--------------------------------------------------")
        print(f"検出された乾燥期間の終了回数: {total_dry_spell_ends} 回")
        print(f"乾燥期間の終了後、次の日に大雨が降った回数: {dry_spell_ends_followed_by_heavy_rain} 回")

        if total_dry_spell_ends > 0:
            percentage = (dry_spell_ends_followed_by_heavy_rain / total_dry_spell_ends) * 100
            print(f"乾燥期間の終了後、次の日に大雨が降る割合: {percentage:.2f} %")
        else:
            print("指定された条件を満たす乾燥期間が見つかりませんでした。")

    except FileNotFoundError:
        print(f"エラー: {file_path} が見つかりません。")
    except Exception as e:
        print(f"処理中にエラーが発生しました: {e}")

if __name__ == '__main__':
    analyze_dry_spell_and_heavy_rain()
