import pandas as pd

# CSVファイルを読み込む
df = pd.read_csv(
    'hijioriAmedas_data.csv',
    header=None,
    encoding='cp932',
    names=[
        '日付', '降水量の合計(mm)', '1時間降水量の最大(mm)', 
        '平均気温(℃)', '最高気温(℃)', '最低気温(℃)', 
        '最大風速(m/s)', '最大風速の風向', '最大瞬間風速(m/s)', 
        '最大瞬間風速の風向', '最深積雪(cm)', '積雪深合計(cm)'
    ]
)

# データ型を変換
df['日付'] = pd.to_datetime(df['日付'], errors='coerce')
df['最高気温(℃)'] = pd.to_numeric(df['最高気温(℃)'], errors='coerce')

# 30℃を超えた日をTrue/Falseで示す列を作成
hot_days = df['最高気温(℃)'] > 30

# 連続日数を計算するためのグループを作成
blocks = (hot_days != hot_days.shift()).cumsum()

# 猛暑日の連続期間のみを抽出
hot_streaks = hot_days[hot_days]

if not hot_streaks.empty:
    # 各連続期間の情報を集計
    streaks_df = hot_streaks.groupby(blocks[hot_days]).agg(
        length=('size'),
        start_date_idx=(lambda x: x.index[0]),
        end_date_idx=(lambda x: x.index[-1])
    )

    # 日付を取得
    streaks_df['start_date'] = df.loc[streaks_df['start_date_idx'], '日付'].values
    streaks_df['end_date'] = df.loc[streaks_df['end_date_idx'], '日付'].values

    # 長さでソート
    streaks_df_sorted = streaks_df.sort_values(by='length', ascending=False)

    # 上位10件をファイルに出力
    output_filename = 'top_10_hot_streaks.txt'
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write("猛暑日（30℃超）の連続期間ランキング (上位10)\n")
        f.write("-" * 45 + "\n")
        
        for i, row in enumerate(streaks_df_sorted.head(10).itertuples(), 1):
            start = row.start_date.strftime('%Y/%m/%d')
            end = row.end_date.strftime('%Y/%m/%d')
            length = int(row.length)
            f.write(f"{i:2d}位: {start} 〜 {end} ({length}日間)\n")

    print(f"上位10件のランキングを '{output_filename}' に保存しました。")

else:
    print("30℃を超えた日はありませんでした。")