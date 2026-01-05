import pandas as pd

# Load the data
file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/hijioriAmedas_data_utf8.csv'
df = pd.read_csv(file_path)

# Convert '年月日' to datetime
df['年月日'] = pd.to_datetime(df['年月日'], format='%Y/%m/%d')

# Convert '最高気温(℃)' to numeric, coercing errors
df['最高気温(℃)'] = pd.to_numeric(df['最高気温(℃)'], errors='coerce')

# Filter for summer months (June, July, August)
df_summer = df[df['年月日'].dt.month.isin([6, 7, 8])]

# This year's summer (2025)
# Note: As of 2025/08/15, we only have partial data for summer 2025.
df_2025_summer = df_summer[df_summer['年月日'].dt.year == 2025]

# Previous 10 years' summer (2015-2024)
df_prev_10_summers = df_summer[(df_summer['年月日'].dt.year >= 2015) & (df_summer['年月日'].dt.year <= 2024)]

# Calculate average maximum temperature
avg_max_temp_2025 = df_2025_summer['最高気温(℃)'].mean()
avg_max_temp_prev_10 = df_prev_10_summers['最高気温(℃)'].mean()

print(f"2025年夏の平均最高気温: {avg_max_temp_2025:.2f}℃")
print(f"過去10年間（2015-2024年）の夏の平均最高気温: {avg_max_temp_prev_10:.2f}℃")

# Compare and print the trend
if avg_max_temp_2025 > avg_max_temp_prev_10:
    diff = avg_max_temp_2025 - avg_max_temp_prev_10
    print(f"今年の夏は、過去10年間の夏と比べて平均最高気温が {diff:.2f}℃ 高い傾向にあります。")
elif avg_max_temp_2025 < avg_max_temp_prev_10:
    diff = avg_max_temp_prev_10 - avg_max_temp_2025
    print(f"今年の夏は、過去10年間の夏と比べて平均最高気温が {diff:.2f}℃ 低い傾向にあります。")
else:
    print("今年の夏は、過去10年間の夏と比べて平均最高気温に変化はありません。")
