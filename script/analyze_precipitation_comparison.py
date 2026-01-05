import pandas as pd

# Load the data
file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/hijioriAmedas_data_utf8.csv'
df = pd.read_csv(file_path)

# Convert '年月日' to datetime
df['年月日'] = pd.to_datetime(df['年月日'], format='%Y/%m/%d')

# Convert '降水量の合計(mm)' to numeric
df['降水量の合計(mm)'] = pd.to_numeric(df['降水量の合計(mm)'], errors='coerce')

# Filter for summer months (June, July, August)
df_summer = df[df['年月日'].dt.month.isin([6, 7, 8])]

# --- Analysis for 2025 ---
df_2025_summer = df_summer[df_summer['年月日'].dt.year == 2025]
total_precip_2025 = df_2025_summer['降水量の合計(mm)'].sum()

# --- Analysis for 2015-2024 ---
df_prev_10_summers = df_summer[(df_summer['年月日'].dt.year >= 2015) & (df_summer['年月日'].dt.year <= 2024)]
# Calculate the average total summer precipitation over the 10-year period
avg_total_precip_prev_10 = df_prev_10_summers.groupby(df_prev_10_summers['年月日'].dt.year)['降水量の合計(mm)'].sum().mean()


print(f"2025年夏（8月15日現在）の合計降水量: {total_precip_2025:.1f}mm")
print(f"過去10年間（2015-2024年）の夏の平均合計降水量: {avg_total_precip_prev_10:.1f}mm")

# Compare and print the trend
if total_precip_2025 > avg_total_precip_prev_10:
    diff = total_precip_2025 - avg_total_precip_prev_10
    percentage = (diff / avg_total_precip_prev_10) * 100 if avg_total_precip_prev_10 > 0 else float('inf')
    print(f"今年の夏は、過去10年間の平均と比べて、現時点での合計降水量が約{percentage:.0f}%多くなっています。")
elif total_precip_2025 < avg_total_precip_prev_10:
    diff = avg_total_precip_prev_10 - total_precip_2025
    percentage = (diff / avg_total_precip_prev_10) * 100 if avg_total_precip_prev_10 > 0 else float('inf')
    print(f"今年の夏は、過去10年間の平均と比べて、現時点での合計降水量が約{percentage:.0f}%少なくなっています。")
else:
    print("今年の夏は、過去10年間の平均と比べて合計降水量に変化はありません。")
