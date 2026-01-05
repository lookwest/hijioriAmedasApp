
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import matplotlib

# 日本語フォントの設定
matplotlib.rcParams['font.family'] = 'Hiragino Sans' # Macの場合
# 他のOSや環境に合わせて 'Meiryo', 'Yu Gothic', 'Noto Sans CJK JP' などを試す

def plot_winter_analysis(df, start_date_str, end_date_str, output_filename):
    """
    指定された期間の気温と積雪量をプロットします。

    Args:
        df (pd.DataFrame): 気象データフレーム
        start_date_str (str): 開始日 (YYYY-MM-DD形式)
        end_date_str (str): 終了日 (YYYY-MM-DD形式)
        output_filename (str): 出力する画像ファイル名
    """
    # 日付列をdatetime型に変換
    df['年月日'] = pd.to_datetime(df['年月日'])

    # 数値以外の列や欠損値が多い列を前処理
    numeric_cols = ['平均気温(℃)', '最高気温(℃)', '最低気温(℃)', '最深積雪(cm)']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 指定期間のデータを抽出
    mask = (df['年月日'] >= start_date_str) & (df['年月日'] <= end_date_str)
    period_df = df.loc[mask].copy()

    if period_df.empty:
        print(f"エラー: {start_date_str} から {end_date_str} までのデータが見つかりません。")
        return

    # グラフの作成
    fig, ax1 = plt.subplots(figsize=(14, 7))

    # 気温のプロット
    ax1.plot(period_df['年月日'], period_df['最高気温(℃)'], label='最高気温(℃)', color='red', alpha=0.7)
    ax1.plot(period_df['年月日'], period_df['平均気温(℃)'], label='平均気温(℃)', color='orange')
    ax1.plot(period_df['年月日'], period_df['最低気温(℃)'], label='最低気温(℃)', color='blue', alpha=0.7)
    ax1.set_xlabel('日付')
    ax1.set_ylabel('気温 (℃)', color='black')
    ax1.tick_params(axis='y', labelcolor='black')
    ax1.legend(loc='upper left')
    ax1.grid(True, linestyle='--', alpha=0.6)

    # x軸のフォーマット
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.xaxis.set_major_locator(mdates.MonthLocator())
    plt.xticks(rotation=45, ha='right')

    # 最深積雪を二重軸でプロット
    ax2 = ax1.twinx()
    ax2.plot(period_df['年月日'], period_df['最深積雪(cm)'], label='最深積雪(cm)', color='green', linestyle='--', linewidth=2)
    ax2.set_ylabel('最深積雪 (cm)', color='green')
    ax2.tick_params(axis='y', labelcolor='green')
    ax2.legend(loc='upper right')

    plt.title(f'{start_date_str} から {end_date_str} の気温と最深積雪の推移')
    fig.tight_layout() # レイアウト調整
    plt.savefig(output_filename)
    plt.close()
    print(f"グラフを {output_filename} に保存しました。")


if __name__ == '__main__':
    # データの読み込み
    try:
        df = pd.read_csv('hijioriAmedas_data_utf8.csv', encoding='utf-8')
    except FileNotFoundError:
        print("エラー: hijioriAmedas_data_utf8.csv が見つかりません。")
        exit()

    # パラメータ設定
    START_DATE = '2015-12-01'
    END_DATE = '2016-03-31'
    OUTPUT_FILE = 'img/2015_2016_winter_temp_snow.png'

    # 分析とプロットの実行
    plot_winter_analysis(df, START_DATE, END_DATE, OUTPUT_FILE)

