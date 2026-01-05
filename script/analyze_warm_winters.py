import pandas as pd
import numpy as np

def analyze_warm_winters(start_year=2000, end_year=2024):
    """
    指定された期間の冬の平均気温を計算し、暖冬の年をランキング形式で出力する。

    Args:
        start_year (int): 分析開始年（冬シーズンの開始年）
        end_year (int): 分析終了年（冬シーズンの開始年）
    """
    # データファイルを読み込む
    try:
        file_path = 'hijioriAmedas_data_utf8.csv'
        df = pd.read_csv(file_path, encoding='utf-8')
    except FileNotFoundError:
        print(f"エラー: {file_path} が見つかりません。")
        return

    # '年月日'をdatetime型に変換し、エラーは無視
    df['年月日'] = pd.to_datetime(df['年月日'], errors='coerce')
    # '平均気温(℃)'を数値型に変換し、エラーはNaNに
    df['平均気温(℃)'] = pd.to_numeric(df['平均気温(℃)'], errors='coerce')
    # '最深積雪(cm)'の欠損値を0で埋め、数値型に変換
    df['最深積雪(cm)'] = df['最深積雪(cm)'].fillna(0)
    df['最深積雪(cm)'] = pd.to_numeric(df['最深積雪(cm)'], errors='coerce')

    # 欠損値を含む行を削除
    df.dropna(subset=['年月日', '平均気温(℃)', '最深積雪(cm)'], inplace=True)

    winter_temps = []
    # end_yearの冬(end_year/12/1-end_year+1/2/28)まで計算するため、end_year-1までループ
    for year in range(start_year, end_year):
        # 冬の期間を定義 (例: 2000年の冬は2000-12-01から2001-02-28)
        start_date = f"{year}-12-01"
        end_date = f"{year + 1}-02-28" # うるう年も考慮し28日までとする

        mask = (df['年月日'] >= start_date) & (df['年月日'] <= end_date)
        winter_df = df.loc[mask]

        if not winter_df.empty:
            avg_temp = winter_df['平均気温(℃)'].mean()
            max_snow_depth = winter_df['最深積雪(cm)'].max() if not winter_df['最深積雪(cm)'].empty else 0
            # yearは冬シーズンの開始年なので、YYYY年冬と表現
            winter_temps.append({'year': f"{year}年冬", 'avg_temp': avg_temp, 'max_snow_depth': max_snow_depth})

    # 平均気温が高い順にソート
    warmest_winters = sorted(winter_temps, key=lambda x: x['avg_temp'], reverse=True)

    # 結果をファイルに出力
    output_path = 'data_files/warm_winters_ranking.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"暖冬ランキング ({start_year}-{end_year-1}年)\n")
        f.write("=" * 30 + "\n")
        # 上位5件を出力
        for i, winter in enumerate(warmest_winters[:5]):
            f.write(f"{i+1}位: {winter['year']} (平均気温: {winter['avg_temp']:.2f} ℃, 最高積雪深: {winter['max_snow_depth']:.0f} cm)\n")
        
        f.write("\n")
        f.write("全期間のランキング:\n")
        for i, winter in enumerate(warmest_winters):
            f.write(f"{i+1:2d}位: {winter['year']} (平均気温: {winter['avg_temp']:.2f} ℃, 最高積雪深: {winter['max_snow_depth']:.0f} cm)\n")


    print(f"分析結果を '{output_path}' に保存しました。")

if __name__ == "__main__":
    analyze_warm_winters(2000, 2025) #2024年の冬(2024/12-2025/2)まで含める
