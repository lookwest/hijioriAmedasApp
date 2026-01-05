
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import eacal
from datetime import timedelta
import numpy as np

# --- 定数 ---
START_YEAR = 1978
END_YEAR = 2024
DATA_FILE = 'hijioriAmedas_data_utf8.csv'
OUTPUT_FILE = 'winter_sekki_analysis.png'
TARGET_SEKKI = ['冬至', '小寒', '大寒', '立春', '雨水'] # 時系列順

# --- 二十四節気の日付範囲をマッピングする辞書を作成 ---
def create_sekki_map(start_year, end_year):
    sekki_map = {}
    cal = eacal.EACal()
    solar_term_names_jp = [
        '立春', '雨水', '啓蟄', '春分', '清明', '穀雨',
        '立夏', '小満', '芒種', '夏至', '小暑', '大暑',
        '立秋', '処暑', '白露', '秋分', '寒露', '霜降',
        '立冬', '小雪', '大雪', '冬至', '小寒', '大寒'
    ]
    for year in range(start_year, end_year + 2):
        try:
            solar_terms = cal.get_annual_solar_terms(year)
            solar_terms_jp = [(solar_term_names_jp[i], term[2].date()) for i, term in enumerate(solar_terms)]
            for i in range(len(solar_terms_jp)):
                sekki_name = solar_terms_jp[i][0]
                start_date = solar_terms_jp[i][1]
                if i + 1 < len(solar_terms_jp):
                    end_date = solar_terms_jp[i+1][1] - timedelta(days=1)
                else:
                    next_year_solar_terms = cal.get_annual_solar_terms(year + 1)
                    end_date = next_year_solar_terms[0][2].date() - timedelta(days=1)
                current_date = start_date
                while current_date <= end_date:
                    sekki_map[current_date] = sekki_name
                    current_date += timedelta(days=1)
        except Exception:
            continue
    return sekki_map

# --- メイン処理 ---
# 1. データ計算
sekki_date_map = create_sekki_map(START_YEAR, END_YEAR)
df = pd.read_csv(DATA_FILE, encoding='utf-8', low_memory=False)
df['年月日'] = pd.to_datetime(df['年月日'], errors='coerce')
cols_to_numeric = ['降水量の合計(mm)', '最深積雪(cm)', '降雪量合計(cm)']
for col in cols_to_numeric:
    df[col] = pd.to_numeric(df[col], errors='coerce')
df.dropna(subset=['年月日', '降水量の合計(mm)'], inplace=True)
df['年月日'] = df['年月日'].dt.date
df['節気'] = df['年月日'].map(sekki_date_map)
df = df[df['節気'].isin(TARGET_SEKKI)]
df.dropna(subset=['節気'], inplace=True)

if not df.empty:
    agg_funcs = {
        '降水量の合計(mm)': 'mean',
        '最深積雪(cm)': 'mean',
        '降雪量合計(cm)': 'mean'
    }
    sekki_analysis = df.groupby('節気').agg(agg_funcs).reset_index()
    sekki_analysis.rename(columns={
        '降水量の合計(mm)': '日平均 降水量(mm)',
        '最深積雪(cm)': '期間平均 最深積雪(cm)',
        '降雪量合計(cm)': '日平均 降雪量(cm)'
    }, inplace=True)
    
    # 2. グラフ作成準備 (時系列にソート)
    sekki_analysis['節気'] = pd.Categorical(sekki_analysis['節気'], categories=TARGET_SEKKI, ordered=True)
    sekki_analysis.sort_values(by='節気', inplace=True)

    # 3. グラフ描画
    fig, ax1 = plt.subplots(figsize=(12, 7))

    # 棒グラフ (降水量と降雪量)
    bar_width = 0.4
    x = np.arange(len(sekki_analysis['節気']))
    bar1 = ax1.bar(x - bar_width/2, sekki_analysis['日平均 降水量(mm)'], bar_width, label='日平均 降水量(mm)', color='#4682B4')
    bar2 = ax1.bar(x + bar_width/2, sekki_analysis['日平均 降雪量(cm)'], bar_width, label='日平均 降雪量(cm)', color='#B0C4DE')
    ax1.set_xlabel('二十四節気', fontsize=12)
    ax1.set_ylabel('降水量(mm) / 降雪量(cm)', fontsize=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(sekki_analysis['節気'])

    # 折れ線グラフ (積雪深)
    ax2 = ax1.twinx()
    line1 = ax2.plot(x, sekki_analysis['期間平均 最深積雪(cm)'], color='#DC143C', linestyle='--', marker='o', label='期間平均 最深積雪(cm)')
    ax2.set_ylabel('積雪の深さ (cm)', fontsize=12, color='#DC143C')
    ax2.tick_params(axis='y', labelcolor='#DC143C')

    # 4. 仕上げ
    plt.title('肘折の冬 "降る雪"と"積もる雪"の関係 (1978-2024年)', fontsize=16)
    # 凡例をまとめる
    lns = [bar1, bar2] + line1
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc='upper left')
    fig.tight_layout()
    
    # 5. 保存
    plt.savefig(OUTPUT_FILE)
    plt.close()
    print(f"グラフを '{OUTPUT_FILE}' として保存しました。")

else:
    print("分析対象となるデータが見つかりませんでした。")
