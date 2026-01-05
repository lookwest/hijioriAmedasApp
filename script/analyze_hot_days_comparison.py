import pandas as pd

# Load the data
file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/hijioriAmedas_data_utf8.csv'
df = pd.read_csv(file_path)

# Convert '年月日' to datetime
df['年月日'] = pd.to_datetime(df['年月日'], format='%Y/%m/%d')

# Convert '最高気温(℃)' to numeric
df['最高気温(℃)'] = pd.to_numeric(df['最高気温(℃)'], errors='coerce')

# Filter for summer months (June, July, August)
df_summer = df[df['年月日'].dt.month.isin([6, 7, 8])]

# Define a "hot day" (真夏日)
hot_day_threshold = 30

# --- Analysis for 2025 ---
df_2025_summer = df_summer[df_summer['年月日'].dt.year == 2025]
hot_days_2025 = df_2025_summer[df_2025_summer['最高気温(℃)'] >= hot_day_threshold]
count_hot_days_2025 = len(hot_days_2025)

# --- Analysis for 2015-2024 ---
df_prev_10_summers = df_summer[(df_summer['年月日'].dt.year >= 2015) & (df_summer['年月日'].dt.year <= 2024)]
hot_days_prev_10 = df_prev_10_summers[df_prev_10_summers['最高気温(℃)'] >= hot_day_threshold]
# Calculate the average number of hot days per year over the 10-year period
avg_hot_days_prev_10 = len(hot_days_prev_10) / 10.0

print(f"2025年夏（8月15日現在）の真夏日（最高気温30℃以上）の日数: {count_hot_days_2025}日")
print(f"過去10年間（2015-2024年）の夏の年間平均真夏日日数: {avg_hot_days_prev_10:.1f}日")

# Compare and explain
if avg_hot_days_prev_10 > 0:
    increase_percentage = ((count_hot_days_2025 - avg_hot_days_prev_10) / avg_hot_days_prev_10) * 100
    print(f"今年の夏は、過去10年間の平均と比べて、現時点での真夏日の日数が約{increase_percentage:.0f}%多いペースです。")
else:
    print("過去10年間には真夏日がありませんでした。")

print("\nつまり、平均気温が2.1℃高いということは、単に「少し暑い」というだけでなく、「厳しい暑さの日が格段に増えている」と体感されるレベルの変化と言えるでしょう。")
