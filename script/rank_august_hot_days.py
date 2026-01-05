import pandas as pd

try:
    # データファイルを読み込み
    df = pd.read_csv('hijioriAmedas_data_utf8.csv', encoding='utf-8')

    # データ型を適切に変換
    df['年月日'] = pd.to_datetime(df['年月日'], errors='coerce')
    df['最高気温(℃)'] = pd.to_numeric(df['最高気温(℃)'], errors='coerce')

    # 重要なデータが欠損している行を削除
    df.dropna(subset=['年月日', '最高気温(℃)'], inplace=True)

    # 8月のデータのみを抽出
    df_august = df[df['年月日'].dt.month == 8].copy()

    # 真夏日（30℃以上）の日にフラグを立てる
    df_august['真夏日'] = df_august['最高気温(℃)'] >= 30

    # 年ごとに真夏日の日数を集計
    yearly_counts = df_august.groupby(df_august['年月日'].dt.year)['真夏日'].sum().reset_index()
    yearly_counts.columns = ['年', '真夏日の日数']
    yearly_counts['年'] = yearly_counts['年'].astype(int)
    yearly_counts['真夏日の日数'] = yearly_counts['真夏日の日数'].astype(int)

    # 日数が多い順に並べ替え
    yearly_counts_sorted = yearly_counts.sort_values(by='真夏日の日数', ascending=False)

    # 順位を追加
    yearly_counts_sorted['順位'] = yearly_counts_sorted['真夏日の日数'].rank(method='min', ascending=False).astype(int)

    # 列の順序を整理
    final_ranking = yearly_counts_sorted[['順位', '年', '真夏日の日数']]

    # 結果をファイルに出力
    output_filename = 'august_hot_days_ranking.txt'
    final_ranking.to_csv(output_filename, sep='\t', index=False)

    print(f"8月の真夏日日数ランキングを作成し、'{output_filename}'に保存しました。")
    print("\n--- 8月の真夏日 日数ランキング ---")
    # 結果を整形して表示
    print(final_ranking.to_string(index=False))

except FileNotFoundError:
    print("エラー: hijioriAmedas_data_utf8.csv が見つかりません。")
except Exception as e:
    print(f"エラーが発生しました: {e}")
