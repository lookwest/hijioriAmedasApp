
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def find_similar_years(df, target_year, target_month, year_range):
    """
    指定された年月の気象データと、過去の指定された範囲の年月を比較し、
    気象傾向が最も類似している年をランキング形式で返します。

    Args:
        df (pd.DataFrame): 気象データフレーム
        target_year (int): 比較の基準となる年
        target_month (int): 比較の基準となる月
        year_range (range): 比較対象となる年の範囲

    Returns:
        pd.DataFrame: 類似度スコアでソートされた年のデータフレーム
    """
    # 日付列をdatetime型に変換
    df['年月日'] = pd.to_datetime(df['年月日'])

    # 比較指標
    metrics = {
        '平均気温(℃)': 'mean',
        '最高気温(℃)': 'mean',
        '最低気温(℃)': 'mean',
        '降水量の合計(mm)': 'sum',
        '降雪量合計(cm)': 'sum',
        '最深積雪(cm)': 'mean', # 月の平均的な積雪状況を見る
        '日照時間(時間)': 'sum'
    }

    # 数値以外の列や欠損値が多い列を前処理
    for col in metrics.keys():
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 基準月のデータを集計
    target_data = df[(df['年月日'].dt.year == target_year) & (df['年月日'].dt.month == target_month)]
    if target_data.empty:
        print(f"エラー: {target_year}年{target_month}月のデータが見つかりません。")
        return None

    target_summary = target_data[list(metrics.keys())].agg(metrics)

    # 比較対象年のデータを集計して比較
    results = []
    for year in year_range:
        if year == target_year:
            continue

        past_data = df[(df['年月日'].dt.year == year) & (df['年月日'].dt.month == target_month)]
        if past_data.empty:
            continue

        past_summary = past_data[list(metrics.keys())].agg(metrics)

        # 全ての指標が揃っているか確認
        if past_summary.isnull().any():
            continue

        results.append({
            'year': year,
            **past_summary.to_dict()
        })

    if not results:
        print("エラー: 比較対象となる過去のデータがありません。")
        return None

    # 結果をデータフレームに変換
    past_df = pd.DataFrame(results).set_index('year')

    # 基準年のデータを追加して、スケーリングの準備
    all_df = pd.concat([past_df, pd.DataFrame(target_summary).T.rename(index={0: target_year})])

    # Min-Maxスケーリングで各指標を正規化
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(all_df)
    scaled_df = pd.DataFrame(scaled_data, index=all_df.index, columns=all_df.columns)

    # 基準年とのユークリッド距離を計算
    target_vector = scaled_df.loc[target_year]
    past_vectors = scaled_df.drop(target_year)

    distances = np.linalg.norm(past_vectors.values - target_vector.values, axis=1)

    # 距離を類似度スコアに変換 (0に近いほど類似)
    similarity_df = pd.DataFrame({'year': past_vectors.index, 'similarity_score': distances})
    similarity_df = similarity_df.sort_values(by='similarity_score').reset_index(drop=True)

    return similarity_df

if __name__ == '__main__':
    # データの読み込み
    try:
        df = pd.read_csv('hijioriAmedas_data_utf8.csv', encoding='utf-8')
    except FileNotFoundError:
        print("エラー: hijioriAmedas_data_utf8.csv が見つかりません。")
        exit()

    # パラメータ設定
    TARGET_YEAR = 2025
    TARGET_MONTH = 12
    # 過去30年間 (1995-2024)
    PAST_YEARS = range(1995, 2025)

    # 類似年を検索
    similar_years_df = find_similar_years(df, TARGET_YEAR, TARGET_MONTH, PAST_YEARS)

    if similar_years_df is not None:
        # 結果を保存
        output_filename = f'data_files/similar_weather_to_{TARGET_YEAR}_{TARGET_MONTH}.csv'
        similar_years_df.to_csv(output_filename, index=False, encoding='utf-8-sig')

        print(f"今年の{TARGET_MONTH}月と天候が似ている年のランキング:")
        print(similar_years_df.head(10))
        print(f"\n詳細なランキングを {output_filename} に保存しました。")
