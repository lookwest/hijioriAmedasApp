
import csv

file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/hijioriAmedas_data.csv'

def find_very_cold_days():
    """
    CSVファイルから最低気温が-15℃未満の日付と気温をリストアップします。
    """
    very_cold_days = []

    try:
        with open(file_path, 'r', encoding='sjis', errors='ignore') as f:
            reader = csv.reader(f)
            next(reader)  # ヘッダーをスキップ

            for row in reader:
                try:
                    if len(row) > 5 and row[5].strip():
                        min_temp = float(row[5])
                        if min_temp < -15:
                            very_cold_days.append((row[0], min_temp))
                except (ValueError, IndexError):
                    continue

        if very_cold_days:
            print("最低気温が-15℃を下回った日:")
            for day in very_cold_days:
                print(f"- 日付: {day[0]}, 気温: {day[1]} °C")
        else:
            print("最低気温が-15℃を下回った日はありませんでした。")

    except FileNotFoundError:
        print(f"エラー: {file_path} が見つかりません。")
    except Exception as e:
        print(f"処理中にエラーが発生しました: {e}")

if __name__ == '__main__':
    find_very_cold_days()
