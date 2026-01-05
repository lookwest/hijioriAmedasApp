
import pandas as pd

# CSVファイルを読み込む
df = pd.read_csv('hijioriAmedas_data_utf8.csv')

# '年月日'列をdatetime型に変換
df['年月日'] = pd.to_datetime(df['年月日'])

# 1981年のデータを抽出
df_1981 = df[df['年月日'].dt.year == 1981]

# 月ごとにグループ化し、各気象情報の統計値を計算
monthly_summary = df_1981.groupby(df_1981['年月日'].dt.month).agg({
    '降水量の合計(mm)': 'sum',
    '平均気温(℃)': 'mean',
    '最高気温(℃)': 'mean',
    '最低気温(℃)': 'mean',
    '最深積雪(cm)': 'max',
    '降雪量合計(cm)': 'sum'
})

# 列名を分かりやすく変更
monthly_summary.columns = [
    '月間降水量合計(mm)',
    '月平均 平均気温(℃)',
    '月平均 最高気温(℃)',
    '月平均 最低気温(℃)',
    '月最大 最深積雪(cm)',
    '月間降雪量合計(cm)'
]

# 月の列を追加
monthly_summary.index.name = '月'

# 結果を表示
print(monthly_summary.round(1))
