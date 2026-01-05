
import csv
import sys

# CSVファイルのパス
file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/hijioriAmedas_data.csv'

def find_max_snow_depth():
    """
    CSVファイルから最大積雪深とその日付を特定して出力します。
    """
    max_snow_depth = -1
    date_of_max_snow_depth = None
    
    try:
        # Shift-JISでファイルを開き、文字化けを無視する
        with open(file_path, 'r', encoding='sjis', errors='ignore') as f:
            reader = csv.reader(f)
            
            # ヘッダー行をスキップ
            try:
                header = next(reader)
            except StopIteration:
                print("エラー: CSVファイルが空か、ヘッダーが読み取れません。")
                return

            # 各行をループして最大値を探す
            for i, row in enumerate(reader):
                try:
                    # 11番目の列（インデックス10）が最深積雪(cm)
                    if len(row) > 10 and row[10].strip():
                        snow_depth = float(row[10])
                        if snow_depth > max_snow_depth:
                            max_snow_depth = snow_depth
                            # 1番目の列（インデックス0）が日付
                            date_of_max_snow_depth = row[0]
                except (ValueError, IndexError):
                    # 数値に変換できない、または列が存在しない行はスキップ
                    # print(f"警告: {i+2}行目のデータをスキップしました。内容: {row}")
                    continue

        if date_of_max_snow_depth:
            print(f"最大積雪深: {int(max_snow_depth)} cm")
            print(f"日付: {date_of_max_snow_depth}")
        else:
            print("積雪データが見つかりませんでした。")

    except FileNotFoundError:
        print(f"エラー: {file_path} が見つかりません。")
    except Exception as e:
        print(f"処理中に予期せぬエラーが発生しました: {e}")

if __name__ == '__main__':
    find_max_snow_depth()
