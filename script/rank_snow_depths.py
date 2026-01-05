
import csv

# 入力CSVファイルと出力テキストファイルのパス
input_file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/hijioriAmedas_data.csv'
output_file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/top_10_snow_depths.txt'

def rank_top_snow_depths():
    """
    CSVファイルから積雪深データを読み込み、トップ10をランキング形式で
    テキストファイルに出力します。
    """
    snow_data = []
    
    try:
        # Shift-JISでファイルを開き、文字化けを無視する
        with open(input_file_path, 'r', encoding='sjis', errors='ignore') as f:
            reader = csv.reader(f)
            
            # 各行をループしてデータを抽出
            for row in reader:
                try:
                    # 11番目の列（インデックス10）が最深積雪(cm)
                    if len(row) > 10 and row[10].strip():
                        snow_depth = float(row[10])
                        # 1番目の列（インデックス0）が日付
                        date = row[0]
                        # 日付と積雪深をタプルでリストに追加
                        snow_data.append((snow_depth, date))
                except (ValueError, IndexError):
                    # 数値に変換できない、または列が存在しない行はスキップ
                    continue

        # 積雪深の降順でソート
        sorted_snow_data = sorted(snow_data, key=lambda x: x[0], reverse=True)
        
        # トップ10をファイルに書き出す
        with open(output_file_path, 'w', encoding='utf-8') as out_f:
            out_f.write("最高積雪深トップ10\n")
            out_f.write("====================\n")
            for i, (depth, date) in enumerate(sorted_snow_data[:10]):
                out_f.write(f"{i+1}位: {int(depth)} cm (日付: {date})\n")
        
        print(f"結果を {output_file_path} に保存しました。")

    except FileNotFoundError:
        print(f"エラー: {input_file_path} が見つかりません。")
    except Exception as e:
        print(f"処理中に予期せぬエラーが発生しました: {e}")

if __name__ == '__main__':
    rank_top_snow_depths()
