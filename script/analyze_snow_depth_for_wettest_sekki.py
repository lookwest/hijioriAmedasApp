
import pandas as pd
import eacal
from datetime import timedelta
import numpy as np

# --- 定数 ---
START_YEAR = 1978
END_YEAR = 2024
DATA_FILE = 'hijioriAmedas_data_utf8.csv'
TARGET_SEKKI = ['小寒', '大寒', '立春', '冬至', '雨水']

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
# 1. 準備
sekki_date_map = create_sekki_map(START_YEAR, END_YEAR)
df = pd.read_csv(DATA_FILE, encoding='utf-8', low_memory=False)

# 2. データ前処理
df['年月日'] = pd.to_datetime(df['年月日'], errors='coerce')
df.dropna(subset=['年月日'], inplace=True)

# 数値データに変換できない値はNaNにする
cols_to_numeric = ['降水量の合計(mm)', '最深積雪(cm)', '降雪量合計(cm)']
for col in cols_to_numeric:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df.dropna(subset=['降水量の合計(mm)'], inplace=True) # 降水量の欠損は除外

# 3. 節気情報の付与とフィルタリング
df['年月日'] = df['年月日'].dt.date
df['節気'] = df['年月日'].map(sekki_date_map)
df = df[df['節気'].isin(TARGET_SEKKI)]
df.dropna(subset=['節気'], inplace=True)

# 4. 集計
if not df.empty:
    # 節気ごとに各指標の「日平均」を計算
    # (期間中の合計値を、その期間の日数で割る)
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

    # 5. 結果表示 (降水量順)
    # カテゴリ型にしてソート順を固定
    sekki_analysis['節気'] = pd.Categorical(sekki_analysis['節気'], categories=TARGET_SEKKI, ordered=True)
    sekki_analysis.sort_values(by='節気', inplace=True)
    
    print("--- 冬の二十四節気別 降水量・積雪深・降雪量 分析 (日平均) ---")
    print(sekki_analysis.to_string(index=False))

else:
    print("分析対象となるデータが見つかりませんでした。")
