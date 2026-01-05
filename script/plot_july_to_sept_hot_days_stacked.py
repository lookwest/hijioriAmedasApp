
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# 日本語フォントの設定
font_path = '/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc' # macOS

# フォントプロパティを設定
font_prop = fm.FontProperties(fname=font_path)

# matplotlibのデフォルトフォントを設定
plt.rcParams['font.family'] = font_prop.get_name()

try:
    # データを読み込み
    df = pd.read_csv('hijioriAmedas_data_utf8.csv', encoding='utf-8')

    # データ型を変換
    df['年月日'] = pd.to_datetime(df['年月日'], errors='coerce')
    df['最高気温(℃)'] = pd.to_numeric(df['最高気温(℃)'], errors='coerce')

    # 欠損値を削除
    df.dropna(subset=['年月日', '最高気温(℃)'], inplace=True)

    # 1978年から2025年までの7月, 8月, 9月のデータを抽出
    df_filtered = df[(df['年月日'].dt.year >= 1978) & (df['年月日'].dt.year <= 2025) & (df['年月日'].dt.month.isin([7, 8, 9]))].copy()

    # 真夏日（30℃以上）のデータを抽出
    hot_days = df_filtered[df_filtered['最高気温(℃)'] >= 30].copy()

    # 年と月を列として追加
    hot_days['year'] = hot_days['年月日'].dt.year
    hot_days['month'] = hot_days['年月日'].dt.month

    # 年と月でグループ化し、日数をカウント
    monthly_counts = hot_days.groupby(['year', 'month']).size().unstack(fill_value=0)

    # 1978年から2025年までのすべての年を含むようにインデックスを再設定
    all_years_index = pd.Index(range(1978, 2026), name='year')
    monthly_counts = monthly_counts.reindex(all_years_index, fill_value=0)
    
    # 9月、8月、7月の順に列を並べ替える（積み上げ順のため）
    if 7 not in monthly_counts.columns: monthly_counts[7] = 0
    if 8 not in monthly_counts.columns: monthly_counts[8] = 0
    if 9 not in monthly_counts.columns: monthly_counts[9] = 0
    monthly_counts = monthly_counts[[7, 8, 9]]
    monthly_counts.columns = ['7月', '8月', '9月']

    # グラフの作成
    fig, ax = plt.subplots(figsize=(18, 8))
    colors = ['#E69F00', '#D55E00', '#8B4513']
    monthly_counts.plot(kind='bar', stacked=True, ax=ax, color=colors)

    # タイトルとラベルを設定
    ax.set_title('7月-9月 真夏日の日数推移 (1978-2025年)', fontproperties=font_prop, fontsize=20)
    ax.set_xlabel('年', fontproperties=font_prop, fontsize=14)
    ax.set_ylabel('真夏日の日数', fontproperties=font_prop, fontsize=14)
    
    # X軸のラベルをすべて表示
    ax.set_xticks(range(len(monthly_counts.index)))
    ax.set_xticklabels(monthly_counts.index, rotation=90, fontsize=8)

    # Y軸の補助線を5日ごとに入れる
    max_days = monthly_counts.sum(axis=1).max()
    y_ticks = np.arange(0, max_days + 5, 5)
    ax.set_yticks(y_ticks)
    ax.yaxis.grid(True, linestyle='--', linewidth=0.5, color='gray')

    # 凡例のフォントを設定
    plt.legend(prop=font_prop)

    # レイアウトを調整
    plt.tight_layout()

    # グラフをファイルに保存
    output_filename = 'july_to_sept_hot_days_stacked.png'
    plt.savefig(output_filename)

    print(f"グラフに補助線を追加し、'{output_filename}' に再度保存しました。")

except FileNotFoundError:
    print(f"エラー: データファイルが見つかりません。")
except Exception as e:
    print(f"グラフ作成中にエラーが発生しました: {e}")
