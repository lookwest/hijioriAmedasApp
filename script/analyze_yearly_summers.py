import pandas as pd

# Load the data
file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/hijioriAmedas_data_utf8.csv'
df = pd.read_csv(file_path)

# Convert columns to appropriate data types
df['年月日'] = pd.to_datetime(df['年月日'], format='%Y/%m/%d')
df['最高気温(℃)'] = pd.to_numeric(df['最高気温(℃)'], errors='coerce')
df['降水量の合計(mm)'] = pd.to_numeric(df['降水量の合計(mm)'], errors='coerce')

# Filter for summer months (June, July, August)
df_summer = df[df['年月日'].dt.month.isin([6, 7, 8])]

# Years to analyze
years_to_analyze = range(2015, 2025)

# Store results
yearly_results = []

# Analyze each year
for year in years_to_analyze:
    df_year_summer = df_summer[df_summer['年月日'].dt.year == year]
    
    # Skip if no data for the year
    if df_year_summer.empty:
        continue
    
    avg_max_temp = df_year_summer['最高気温(℃)'].mean()
    hot_days = (df_year_summer['最高気温(℃)'] >= 30).sum()
    total_precip = df_year_summer['降水量の合計(mm)'].sum()
    
    yearly_results.append({
        '年': year,
        '夏の平均最高気温(℃)': f"{avg_max_temp:.2f}",
        '夏の真夏日日数': hot_days,
        '夏の合計降水量(mm)': f"{total_precip:.1f}"
    })

# Create a DataFrame from the results
results_df = pd.DataFrame(yearly_results)

# Save the DataFrame to a CSV file
output_file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/yearly_summer_analysis_2015-2024.csv'
results_df.to_csv(output_file_path, index=False, encoding='utf-8-sig')

print(f"過去10年間の各年の夏の分析結果を {output_file_path} に保存しました。")