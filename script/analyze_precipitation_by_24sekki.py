import pandas as pd
import eacal
from datetime import timedelta

# --- 定数 ---
START_YEAR = 1978
END_YEAR = 2024
DATA_FILE = 'hijioriAmedas_data_utf8.csv'

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
            # 3番目の要素(term[2])が日付オブジェクトだった
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
# 1. 節気マッピングの作成
sekki_date_map = create_sekki_map(START_YEAR, END_YEAR)

# 2. 気象データの読み込みと前処理
df = pd.read_csv(DATA_FILE, encoding='utf-8', low_memory=False)
df.dropna(subset=['年月日', '降水量の合計(mm)'], inplace=True)
df['年月日'] = pd.to_datetime(df['年月日'], errors='coerce')
df.dropna(subset=['年月日'], inplace=True)

# 3. 分析対象年数の計算
analysis_years = df['年月日'].dt.year.nunique()

# 4. 節気情報の付与
df['年月日'] = df['年月日'].dt.date
df['節気'] = df['年月日'].map(sekki_date_map)
df.dropna(subset=['節気'], inplace=True)

# 5. 集計
if not df.empty:
    sekki_precipitation = df.groupby('節気')['降水量の合計(mm)'].sum().reset_index()
    sekki_precipitation['年平均降水量(mm)'] = sekki_precipitation['降水量の合計(mm)'] / analysis_years

    # 6. 結果表示
    sorted_sekki_names = [
        '立春', '雨水', '啓蟄', '春分', '清明', '穀雨',
        '立夏', '小満', '芒種', '夏至', '小暑', '大暑',
        '立秋', '処暑', '白露', '秋分', '寒露', '霜降',
        '立冬', '小雪', '大雪', '冬至', '小寒', '大寒'
    ]
    sekki_precipitation['節気'] = pd.Categorical(sekki_precipitation['節気'], categories=sorted_sekki_names, ordered=True)
    precipitation_ranking = sekki_precipitation.sort_values(by='年平均降水量(mm)', ascending=False)

    print("--- 二十四節気別 年平均降水量ランキング (1978-2024年) ---")
    print(precipitation_ranking[['節気', '年平均降水量(mm)']].to_string(index=False))
else:
    print("分析対象となるデータが見つかりませんでした。")