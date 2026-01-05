
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import eacal
from datetime import timedelta

# --- 定数 ---
START_YEAR = 1978
END_YEAR = 2024
DATA_FILE = 'hijioriAmedas_data_utf8.csv'
OUTPUT_FILE = 'precipitation_by_24sekki.png'

# --- 二十四節気の日付範囲をマッピングする辞書を作成 (前回のスクリプトと同じ) ---
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
df.dropna(subset=['年月日', '降水量の合計(mm)'], inplace=True)
df['年月日'] = pd.to_datetime(df['年月日'], errors='coerce')
df.dropna(subset=['年月日'], inplace=True)
analysis_years = df['年月日'].dt.year.nunique()
df['年月日'] = df['年月日'].dt.date
df['節気'] = df['年月日'].map(sekki_date_map)
df.dropna(subset=['節気'], inplace=True)

if not df.empty:
    sekki_precipitation = df.groupby('節気')['降水量の合計(mm)'].sum().reset_index()
    sekki_precipitation['年平均降水量(mm)'] = sekki_precipitation['降水量の合計(mm)'] / analysis_years
    
    # 2. グラフ作成の準備 (暦順にソート)
    sorted_sekki_names = [
        '立春', '雨水', '啓蟄', '春分', '清明', '穀雨',
        '立夏', '小満', '芒種', '夏至', '小暑', '大暑',
        '立秋', '処暑', '白露', '秋分', '寒露', '霜降',
        '立冬', '小雪', '大雪', '冬至', '小寒', '大寒'
    ]
    sekki_precipitation['節気'] = pd.Categorical(sekki_precipitation['節気'], categories=sorted_sekki_names, ordered=True)
    sekki_precipitation.sort_values(by='節気', inplace=True)

    # 3. グラフの描画
    plt.figure(figsize=(15, 8))
    plt.bar(sekki_precipitation['節気'], sekki_precipitation['年平均降水量(mm)'])
    
    plt.title('肘折 二十四節気別 年平均降水量 (1978-2024年)', fontsize=16)
    plt.xlabel('二十四節気', fontsize=12)
    plt.ylabel('年平均降水量 (mm)', fontsize=12)
    plt.xticks(rotation=70)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # 4. グラフの保存
    plt.savefig(OUTPUT_FILE)
    plt.close()
    print(f"グラフを '{OUTPUT_FILE}' として保存しました。")

else:
    print("分析対象となるデータが見つかりませんでした。")
