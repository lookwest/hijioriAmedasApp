
import pandas as pd
from datetime import datetime

# Load the data
try:
    df = pd.read_csv('hijioriAmedas_data_utf8.csv', encoding='utf-8')
except FileNotFoundError:
    print("Error: The file 'hijioriAmedas_data_utf8.csv' was not found.")
    exit()

# Rename columns for easier access
df.columns = [
    '年月日', '降水量の合計', '1時間降水量の最大', '平均気温', '最高気温', '最低気温',
    '最大瞬間風速', '最大瞬間風速の風向', '最多風向', '日照時間', '降雪量合計', '最深積雪'
]

# Convert date column to datetime objects
df['年月日'] = pd.to_datetime(df['年月日'], format='%Y/%m/%d')

# Convert wind speed column to numeric, coercing errors
df['最大瞬間風速'] = pd.to_numeric(df['最大瞬間風速'], errors='coerce')

# Drop rows with NaN in '最大瞬間風速'
df.dropna(subset=['最大瞬間風速'], inplace=True)

# Filter for the last 30 years
thirty_years_ago = datetime.now() - pd.DateOffset(years=30)
df_last_30_years = df[df['年月日'] >= thirty_years_ago]

# Sort by wind speed and get the top 10
top_10_windy_days = df_last_30_years.sort_values(by='最大瞬間風速', ascending=False).head(10)

# Print the result
print("過去30年間で風が強かった日トップ10:")
print(top_10_windy_days[['年月日', '最大瞬間風速']].to_string(index=False))
