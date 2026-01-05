
import pandas as pd

file_path = 'hijioriAmedas_data_utf8.csv'

# CSVファイルを読み込む
try:
    df = pd.read_csv(file_path, encoding='utf-8')
except FileNotFoundError:
    print(f"エラー: ファイル '{file_path}' が見つかりません。")
    exit()

# '年月日'列をdatetime型に変換
df['年月日'] = pd.to_datetime(df['年月日'], errors='coerce')
df = df.dropna(subset=['年月日'])

# '降雪量合計(cm)'列が存在するか確認
if '降雪量合計(cm)' not in df.columns:
    print("エラー: '降雪量合計(cm)'列が見つかりません。")
    exit()

# '降雪量合計(cm)'が0より大きいデータのみに絞り込む
snow_days = df[df['降雪量合計(cm)'] > 0]

first_snow_dates = []

# データが存在する年を取得
start_year = snow_days['年月日'].dt.year.min()
end_year = snow_days['年月日'].dt.year.max()

for year in range(start_year, end_year):
    # 8月1日から翌年7月31日までを1シーズンとする
    season_start = pd.to_datetime(f'{year}-08-01')
    season_end = pd.to_datetime(f'{year+1}-07-31')
    
    season_snow_days = snow_days[(snow_days['年月日'] >= season_start) & (snow_days['年月日'] <= season_end)]
    
    if not season_snow_days.empty:
        # シーズン最初の降雪日を取得
        first_snow_day = season_snow_days.iloc[0]
        first_snow_dates.append({
            'season_year': year,
            'first_snow_date': first_snow_day['年月日']
        })

if not first_snow_dates:
    print("降雪データが見つかりませんでした。")
    exit()

# 初雪日を格納したDataFrameを作成
first_snow_df = pd.DataFrame(first_snow_dates)

# 月日でソートするために、年をダミーの年(例: 2000年)に統一して比較
first_snow_df['sort_key'] = first_snow_df['first_snow_date'].apply(lambda d: d.replace(year=2000))

# 最も速い初雪日を取得
earliest_first_snow = first_snow_df.loc[first_snow_df['sort_key'].idxmin()]

season = int(earliest_first_snow['season_year'])
date = earliest_first_snow['first_snow_date'].strftime('%Y年%m月%d日')

print(f"初雪が最も速かったシーズン: {season}年〜{season+1}年")
print(f"その時の初雪日: {date}")
