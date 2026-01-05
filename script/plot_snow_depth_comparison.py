import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib

# データファイルを読み込む
file_path = 'hijioriAmedas_data_utf8.csv'
df = pd.read_csv(file_path, encoding='utf-8')

# データの前処理
df['年月日'] = pd.to_datetime(df['年月日'])
df['最深積雪(cm)'] = pd.to_numeric(df['最深積雪(cm)'], errors='coerce').fillna(0)

# 比較対象の年
target_years = [2018, 2005, 2013, 2012, 1986]

plt.figure(figsize=(15, 8))

# 各年についてループ
for year in target_years:
    # 冬の期間を定義 (前年の11月1日から当年の4月30日まで)
    start_date = f'{year-1}-11-01'
    end_date = f'{year}-04-30'
    
    winter_df = df[(df['年月日'] >= start_date) & (df['年月日'] <= end_date)].copy()
    
    # 冬の始まりからの日数を計算
    winter_df['冬の日数'] = (winter_df['年月日'] - pd.to_datetime(start_date)).dt.days
    
    # 2018年を強調してプロット
    if year == 2018:
        plt.plot(winter_df['冬の日数'], winter_df['最深積雪(cm)'], label=f'{year} (445cm)', linewidth=3, zorder=5)
    else:
        max_snow = df[df['年月日'].dt.year == year]['最深積雪(cm)'].max()
        plt.plot(winter_df['冬の日数'], winter_df['最深積雪(cm)'], label=f'{year} ({int(max_snow)}cm)', alpha=0.7)

# グラフの装飾
plt.title('過去の豪雪年との積雪推移比較 (肘折)', fontsize=16)
plt.xlabel('冬の始まりからの日数 (11月1日を0日目とする)')
plt.ylabel('最深積雪(cm)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlim(left=30) # 11月は省略して12月から表示
plt.xticks(
    ticks=[30, 61, 92, 120, 151], 
    labels=['12月', '1月', '2月', '3月', '4月']
)

# グラフを保存
output_path = 'snow_depth_comparison.png'
plt.savefig(output_path)

print(f"グラフを {output_path} に保存しました。")
