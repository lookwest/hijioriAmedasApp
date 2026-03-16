import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# 設定
file_path = 'hijioriAmedas_data_utf8.csv'
output_image_path = 'img/january_2026_snow_depth.png'
output_text_path = 'data_files/january_2026_snow_depth_summary.txt'

def plot_january_2026_snow_depth():
    try:
        # CSVを読み込む
        df = pd.read_csv(file_path, encoding='utf-8')
        
        # '年月日'列をdatetime型に変換
        df['年月日'] = pd.to_datetime(df['年月日'], errors='coerce')
        
        # '最深積雪(cm)'列を数値に変換
        df['最深積雪(cm)'] = pd.to_numeric(df['最深積雪(cm)'], errors='coerce')
        
        # 2026年1月のデータを抽出
        start_date = datetime(2026, 1, 1)
        end_date = datetime(2026, 1, 31)
        january_data = df[(df['年月日'] >= start_date) & (df['年月日'] <= end_date)].copy()
        
        if january_data.empty:
            print("2026年1月のデータが見つかりませんでした。")
            return

        # 日付でソート
        january_data.sort_values(by='年月日', inplace=True)

        # グラフの設定
        plt.style.use('default')
        plt.rcParams['font.sans-serif'] = ['Hiragino Sans']
        plt.rcParams['axes.grid'] = True

        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 積雪深のプロット
        ax.plot(january_data['年月日'], january_data['最深積雪(cm)'], marker='o', linestyle='-', color='blue', label='最深積雪')
        
        # ラベルとタイトル
        ax.set_xlabel('日付')
        ax.set_ylabel('最深積雪 (cm)')
        ax.set_title('2026年1月 肘折のアメダス積雪深推移')
        
        # X軸のフォーマット（日のみ表示）
        plt.xticks(january_data['年月日'], [d.strftime('%d') for d in january_data['年月日']])
        ax.set_xlabel('日')
        
        plt.legend()
        plt.tight_layout()

        # 画像として保存
        os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
        plt.savefig(output_image_path)
        print(f"グラフを {output_image_path} に保存しました。")

        # 分析結果のテキスト保存
        max_snow = january_data['最深積雪(cm)'].max()
        max_snow_date = january_data.loc[january_data['最深積雪(cm)'].idxmax(), '年月日'].strftime('%Y-%m-%d')
        avg_snow = january_data['最深積雪(cm)'].mean()
        min_snow = january_data['最深積雪(cm)'].min()
        min_snow_date = january_data.loc[january_data['最深積雪(cm)'].idxmin(), '年月日'].strftime('%Y-%m-%d')

        summary = [
            "2026年1月 肘折アメダス積雪深分析結果",
            "====================================",
            f"最大積雪深: {max_snow:.1f} cm (観測日: {max_snow_date})",
            f"最小積雪深: {min_snow:.1f} cm (観測日: {min_snow_date})",
            f"平均積雪深: {avg_snow:.1f} cm",
            "------------------------------------",
            "日ごとのデータ:",
        ]
        for index, row in january_data.iterrows():
            summary.append(f"{row['年月日'].strftime('%Y-%m-%d')}: {row['最深積雪(cm)']} cm")

        os.makedirs(os.path.dirname(output_text_path), exist_ok=True)
        with open(output_text_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(summary))
        print(f"分析結果を {output_text_path} に保存しました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == '__main__':
    plot_january_2026_snow_depth()
