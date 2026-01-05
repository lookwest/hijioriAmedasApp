import pandas as pd

# データの読み込み
df = pd.read_csv('hijioriAmedas_data_utf8.csv', low_memory=False)

# 分析対象の列
precip_col = '降水量の合計(mm)'
snowfall_col = '降雪量合計(cm)'

# データクリーニング
df[precip_col] = pd.to_numeric(df[precip_col], errors='coerce')
df[snowfall_col] = pd.to_numeric(df[snowfall_col], errors='coerce')

# --- 分析期間のフィルタリング ---
# 降雪量が0より大きい日（雪が降った日）のみを対象とする
snowy_days_df = df[df[snowfall_col] > 0].copy()

# 両方の列に有効な数値がある行だけを抽出
cleaned_df = snowy_days_df.dropna(subset=[precip_col, snowfall_col])

# 相関係数の計算
correlation = cleaned_df[precip_col].corr(cleaned_df[snowfall_col])

# 結果の表示
print("--- 降水量と降雪量の相関分析 (降雪があった日のみ) ---")
print(f"対象期間: 1978年〜2024年")
print(f"分析対象データ数: {len(cleaned_df)}日")
print(f"降水量と降雪量の相関係数: {correlation:.4f}")

if correlation > 0.9:
    print("\n結論: 非常に強い正の相関があります。")
elif correlation > 0.7:
    print("\n結論: 強い正の相関があります。")
elif correlation > 0.4:
    print("\n結論: 中程度の正の相関があります。")
else:
    print("\n結論: 相関は弱いか、ほとんどありません。")