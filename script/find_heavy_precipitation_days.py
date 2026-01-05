
import csv

file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/hijioriAmedas_data.csv'

def find_heavy_precipitation_days():
    """
    CSVファイルから1日の降水量が100mmを超えた日付と降水量をリストアップします。
    """
    heavy_precipitation_days = []

    try:
        with open(file_path, 'r', encoding='sjis', errors='ignore') as f:
            reader = csv.reader(f)
            next(reader)  # ヘッダーをスキップ

            for row in reader:
                try:
                    # 降水量の合計(mm) は2列目 (インデックス 1)
                    if len(row) > 1 and row[1].strip():
                        precipitation = float(row[1])
                        if precipitation > 100:
                            heavy_precipitation_days.append((row[0], precipitation))
                except (ValueError, IndexError):
                    continue

        if heavy_precipitation_days:
            print("1日の降水量が100mmを超えた日:")
            for day in heavy_precipitation_days:
                print(f"- 日付: {day[0]}, 降水量: {day[1]:.1f} mm")
        else:
            print("1日の降水量が100mmを超えた日はありませんでした。")

    except FileNotFoundError:
        print(f"エラー: {file_path} が見つかりません。")
    except Exception as e:
        print(f"処理中にエラーが発生しました: {e}")

if __name__ == '__main__':
    find_heavy_precipitation_days()
