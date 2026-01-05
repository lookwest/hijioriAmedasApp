
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

# 2025年のデータのみに絞り込む
df_2025 = df[df['日付'].dt.year == 2025].copy()

# 30℃を超えた日をTrue/Falseで示す列を作成
hot_days = df_2025['最高気温(℃)'] > 30

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
    streaks_df['start_date'] = df_2025.loc[streaks_df['start_date_idx'], '日付'].values
    streaks_df['end_date'] = df_2025.loc[streaks_df['end_date_idx'], '日付'].values

    # 長さでソート
    streaks_df_sorted = streaks_df.sort_values(by='length', ascending=False)

    print("今年（2025年）の猛暑日（30℃超）の連続記録:")
    print("-" * 45)
    
    for row in streaks_df_sorted.itertuples():
        start = row.start_date.strftime('%Y/%m/%d')
        end = row.end_date.strftime('%Y/%m/%d')
        length = int(row.length)
        print(f"{start} 〜 {end} ({length}日間)")

    longest_streak = streaks_df_sorted.iloc[0]
    longest_length = int(longest_streak.length)
    print(f"\n最長の連続日数は {longest_length} 日間です。")

else:
    print("今年（2025年）はまだ30℃を超えた日はありません。")
