
import csv

file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/hijioriAmedas_data.csv'

def find_extreme_hot_days():
    """
    CSVファイルから最高気温が35℃以上になった日付と気温をリストアップします。
    """
    extreme_hot_days = []

    try:
        with open(file_path, 'r', encoding='sjis', errors='ignore') as f:
            reader = csv.reader(f)

            for row in reader:
                try:
                    # 最高気温は5列目 (インデックス4)
                    if len(row) > 4 and row[4].strip():
                        max_temp = float(row[4])
                        if max_temp >= 35:
                            extreme_hot_days.append((row[0], max_temp))
                except (ValueError, IndexError):
                    continue

        if extreme_hot_days:
            print("最高気温が35℃以上になった日:")
            for day in extreme_hot_days:
                print(f"- 日付: {day[0]}, 気温: {day[1]} °C")
        else:
            print("最高気温が35℃以上になった日はありませんでした。")

    except FileNotFoundError:
        print(f"エラー: {file_path} が見つかりません。")
    except Exception as e:
        print(f"処理中にエラーが発生しました: {e}")

if __name__ == '__main__':
    find_extreme_hot_days()
