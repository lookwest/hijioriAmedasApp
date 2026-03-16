import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# 設定
file_path = 'hijioriAmedas_data_utf8.csv'
output_image_path = 'img/monthly_max_temp_boxplot.png'

def plot_monthly_temp_boxplot():
    try:
        # CSVを読み込む
        df = pd.read_csv(file_path, encoding='utf-8')
        
        # '年月日'列をdatetime型に変換
        df['年月日'] = pd.to_datetime(df['年月日'], errors='coerce')
        
        # '最高気温(℃)'列を数値に変換
        df['最高気温(℃)'] = pd.to_numeric(df['最高気温(℃)'], errors='coerce')
        
        # 直近10年間のデータを抽出
        current_year = datetime.now().year
        df_last_10_years = df[df['年月日'].dt.year >= (current_year - 10)].copy()
        
        # 月の列を追加
        df_last_10_years['月'] = df_last_10_years['年月日'].dt.month
        
        if df_last_10_years.empty:
            print("データが見つかりませんでした。")
            return

        # グラフの設定
        plt.style.use('default')
        plt.rcParams['font.sans-serif'] = ['Hiragino Sans']
        plt.rcParams['axes.grid'] = True

        plt.figure(figsize=(12, 7))
        
        # 箱ひげ図の作成
        sns.boxplot(x='月', y='最高気温(℃)', data=df_last_10_years, palette='coolwarm')
        
        # ラベルとタイトル
        plt.xlabel('月')
        plt.ylabel('最高気温 (℃)')
        plt.title(f'過去10年間 月ごとの最高気温分布 (箱ひげ図)')
        
        plt.tight_layout()

        # 画像として保存
        os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
        plt.savefig(output_image_path)
        print(f"箱ひげ図を {output_image_path} に保存しました。")

        # publicディレクトリにもコピー（デプロイ用）
        public_path = os.path.join('public', os.path.basename(output_image_path))
        os.makedirs('public', exist_ok=True)
        plt.savefig(public_path)
        print(f"デプロイ用に {public_path} にも保存しました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == '__main__':
    plot_monthly_temp_boxplot()
