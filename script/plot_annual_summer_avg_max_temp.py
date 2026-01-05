
import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the CSV file
file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/yearly_summer_analysis_2015-2024.csv'
df_results = pd.read_csv(file_path, encoding='utf-8-sig')

years = df_results['年']
temperatures = df_results['夏の平均最高気温(℃)']

output_image_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/annual_summer_avg_max_temp.png'

plt.figure(figsize=(12, 6))
plt.plot(years, temperatures, marker='o', linestyle='-', color='skyblue')

plt.title('Average of Annual Summer Maximum Temperatures')
plt.xlabel('Year')
plt.ylabel('Average Max Temperature (°C)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(output_image_path)
print(f"グラフが {output_image_path} に保存されました。")
