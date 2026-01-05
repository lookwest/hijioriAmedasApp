

import pandas as pd
from datetime import timedelta

file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/hijioriAmedas_data.csv'

def analyze_heavy_rain_patterns(heavy_rain_threshold_mm=50, days_before=3, days_after=3):
    """
    大雨の日の前後における気象要素の傾向を分析します。
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

        # 日付をdatetimeオブジェクトに変換
        df['日付'] = pd.to_datetime(df['日付'], errors='coerce')
        df.dropna(subset=['日付'], inplace=True)

        # 数値データに変換（エラーはNaNとし、後でdropna）
        df['降水量の合計(mm)'] = pd.to_numeric(df['降水量の合計(mm)'], errors='coerce').fillna(0)
        df['平均気温(℃)'] = pd.to_numeric(df['平均気温(℃)'], errors='coerce')
        df['最大風速(m/s)'] = pd.to_numeric(df['最大風速(m/s)'], errors='coerce')
        # 風向きのクリーニング: 空白やハイフンをNaNに変換
        df['最大風速の風向'] = df['最大風速の風向'].replace({'-': pd.NA, '': pd.NA})

        # 日付でソート
        df.sort_values(by='日付', inplace=True)
        df.reset_index(drop=True, inplace=True)

        heavy_rain_days_indices = df[df['降水量の合計(mm)'] >= heavy_rain_threshold_mm].index.tolist()

        if not heavy_rain_days_indices:
            print(f"降水量が {heavy_rain_threshold_mm}mm 以上の日が見つかりませんでした。")
            return

        print(f"分析対象: 1日の降水量が {heavy_rain_threshold_mm}mm 以上の日")
        print(f"--------------------------------------------------")

        for idx in heavy_rain_days_indices:
            heavy_rain_date = df.loc[idx, '日付']
            heavy_rain_prec = df.loc[idx, '降水量の合計(mm)']
            print(f"\n大雨の日: {heavy_rain_date.strftime('%Y/%m/%d')} (降水量: {heavy_rain_prec}mm)")

            # 前の期間の分析
            start_idx_before = max(0, idx - days_before)
            end_idx_before = idx - 1
            if start_idx_before <= end_idx_before:
                df_before = df.loc[start_idx_before:end_idx_before].copy()
                print(f"  - 前 {days_before} 日間の傾向 ({df_before['日付'].min().strftime('%Y/%m/%d')} - {df_before['日付'].max().strftime('%Y/%m/%d')}):")
                print(f"    平均気温: {df_before['平均気温(℃)'].mean():.2f} °C")
                print(f"    平均最大風速: {df_before['最大風速(m/s)'].mean():.2f} m/s")
                # 最も多い風向き
                most_common_wind_before = df_before['最大風速の風向'].mode()
                if not most_common_wind_before.empty:
                    print(f"    主要な風向き: {most_common_wind_before.iloc[0]}")
                else:
                    print(f"    主要な風向き: N/A")
            else:
                print(f"  - 前 {days_before} 日間のデータがありませんでした。")

            # 後の期間の分析
            start_idx_after = idx + 1
            end_idx_after = min(len(df) - 1, idx + days_after)
            if start_idx_after <= end_idx_after:
                df_after = df.loc[start_idx_after:end_idx_after].copy()
                print(f"  - 後 {days_after} 日間の傾向 ({df_after['日付'].min().strftime('%Y/%m/%d')} - {df_after['日付'].max().strftime('%Y/%m/%d')}):")
                print(f"    平均気温: {df_after['平均気温(℃)'].mean():.2f} °C")
                print(f"    平均最大風速: {df_after['最大風速(m/s)'].mean():.2f} m/s")
                # 最も多い風向き
                most_common_wind_after = df_after['最大風速の風向'].mode()
                if not most_common_wind_after.empty:
                    print(f"    主要な風向き: {most_common_wind_after.iloc[0]}")
                else:
                    print(f"    主要な風向き: N/A")
            else:
                print(f"  - 後 {days_after} 日間のデータがありませんでした。")

    except FileNotFoundError:
        print(f"エラー: {file_path} が見つかりません。")
    except Exception as e:
        print(f"処理中にエラーが発生しました: {e}")

if __name__ == '__main__':
    analyze_heavy_rain_patterns()

