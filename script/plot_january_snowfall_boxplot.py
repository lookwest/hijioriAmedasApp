import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# 設定
file_path = 'hijioriAmedas_data_utf8.csv'
output_image_path = 'img/january_snowfall_comparison_boxplot.png'

def plot_january_snowfall_boxplot():
    try:
        # CSVを読み込む
        df = pd.read_csv(file_path, encoding='utf-8')
        
        # '年月日'列をdatetime型に変換
        df['年月日'] = pd.to_datetime(df['年月日'], errors='coerce')
        
        # '降雪量合計(cm)'列を数値に変換
        df['降雪量合計(cm)'] = pd.to_numeric(df['降雪量合計(cm)'], errors='coerce')
        
        # 1月のデータのみ抽出
        january_df = df[df['年月日'].dt.month == 1].copy()
        
        # 年の列を追加
        january_df['年'] = january_df['年月日'].dt.year
        
        # 直近10年間に絞る (2017年〜2026年)
        current_year = 2026
        start_year = current_year - 9
        df_plot = january_df[january_df['年'] >= start_year].copy()
        
        if df_plot.empty:
            print("データが見つかりませんでした。")
            return

        # グラフの設定
        plt.style.use('default')
        plt.rcParams['font.sans-serif'] = ['Hiragino Sans']
        plt.rcParams['axes.grid'] = True

        plt.figure(figsize=(14, 8))
        
        # 箱ひげ図の作成
        # 2026年を目立たせるために色を分ける
        colors = ['red' if y == 2026 else 'lightgreen' for y in sorted(df_plot['年'].unique())]
        sns.boxplot(x='年', y='降雪量合計(cm)', data=df_plot, palette=colors)
        
        # ラベルとタイトル
        plt.xlabel('年')
        plt.ylabel('日降雪量 (cm)')
        plt.title(f'1月の日降雪量分布の年次比較 (過去10年間)')
        
        plt.tight_layout()

        # 画像として保存
        os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
        plt.savefig(output_image_path)
        print(f"箱ひげ図を {output_image_path} に保存しました。")

        # publicディレクトリにもコピー
        public_path = os.path.join('public', os.path.basename(output_image_path))
        os.makedirs('public', exist_ok=True)
        plt.savefig(public_path)
        print(f"デプロイ用に {public_path} にも保存しました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == '__main__':
    plot_january_snowfall_boxplot()
