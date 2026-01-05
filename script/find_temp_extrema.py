
import csv

file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/hijioriAmedas_data.csv'

def find_temperature_extremes():
    """
    CSVファイルから最高気温と最低気温の最大値・最小値とその日付を特定して出力します。
    """
    max_temp = -999
    date_of_max_temp = None
    min_temp = 999
    date_of_min_temp = None

    try:
        with open(file_path, 'r', encoding='sjis', errors='ignore') as f:
            reader = csv.reader(f)
            next(reader)  # ヘッダーをスキップ

            for row in reader:
                try:
                    if len(row) > 6:
                        # 最高気温の処理
                        if row[4].strip():
                            current_max_temp = float(row[4])
                            if current_max_temp > max_temp:
                                max_temp = current_max_temp
                                date_of_max_temp = row[0]
                        
                        # 最低気温の処理
                        if row[5].strip():
                            current_min_temp = float(row[5])
                            if current_min_temp < min_temp:
                                min_temp = current_min_temp
                                date_of_min_temp = row[0]

                except (ValueError, IndexError):
                    continue

        if date_of_max_temp and date_of_min_temp:
            print(f"最高気温: {max_temp} °C")
            print(f"日付: {date_of_max_temp}")
            print(f"最低気温: {min_temp} °C")
            print(f"日付: {date_of_min_temp}")
        else:
            print("気温データが見つかりませんでした。")

    except FileNotFoundError:
        print(f"エラー: {file_path} が見つかりません。")
    except Exception as e:
        print(f"処理中にエラーが発生しました: {e}")

if __name__ == '__main__':
    find_temperature_extremes()
