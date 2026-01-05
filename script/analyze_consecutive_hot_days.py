
import pandas as pd

# 対象年
TARGET_YEAR = 2025

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

# 対象年のデータを抽出
df_year = df[df['日付'].dt.year == TARGET_YEAR].copy()

# 30℃を超えた日をTrue/Falseで示す列を作成
hot_days = df_year['最高気温(℃)'] > 30

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
    streaks_df['start_date'] = df_year.loc[streaks_df['start_date_idx'], '日付'].values
    streaks_df['end_date'] = df_year.loc[streaks_df['end_date_idx'], '日付'].values

    # 長さでソート
    streaks_df_sorted = streaks_df.sort_values(by='length', ascending=False)

    if len(streaks_df_sorted) > 1:
        second_longest = streaks_df_sorted.iloc[1]
        start_date = second_longest['start_date']
        end_date = second_longest['end_date']
        length = second_longest['length']

        print(f"{TARGET_YEAR}年の2番目に長い猛暑日（30℃超）の連続期間は、")
        print(f"開始日: {start_date.strftime('%Y/%m/%d')}")
        print(f"終了日: {end_date.strftime('%Y/%m/%d')}")
        print(f"連続日数: {int(length)} 日間")
    else:
        print(f"{TARGET_YEAR}年には、猛暑日の連続期間は1つしかありませんでした。")
else:
    print(f"{TARGET_YEAR}年には30℃を超えた日はありませんでした。")
