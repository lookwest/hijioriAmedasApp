import csv
from datetime import datetime

file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/hijioriAmedas_data_utf8.csv'

def find_longest_dry_spell():
    """
    CSVファイルから降水量が0だった最長の連続日数とその期間を特定します。
    """
    longest_streak = 0
    current_streak = 0
    start_of_longest_streak_date = None
    end_of_longest_streak_date = None
    start_of_current_streak_date = None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)  # ヘッダーを読み込む

            # ヘッダーから列のインデックスを取得
            try:
                date_col_index = header.index('年月日')
                precip_col_index = header.index('降水量の合計(mm)')
            except ValueError as e:
                print(f"エラー: 必要な列が見つかりません - {e}")
                return

            end_of_current_streak_date = None

            for row in reader:
                try:
                    date_str = row[date_col_index]
                    # 日付形式が YYYY/MM/DD であることを確認
                    datetime.strptime(date_str, '%Y/%m/%d')
                    
                    precipitation_str = row[precip_col_index].strip()
                    precipitation = float(precipitation_str) if precipitation_str else 0

                    if precipitation == 0:
                        current_streak += 1
                        if current_streak == 1:
                            start_of_current_streak_date = date_str
                        end_of_current_streak_date = date_str
                    else:
                        if current_streak > longest_streak:
                            longest_streak = current_streak
                            start_of_longest_streak_date = start_of_current_streak_date
                            end_of_longest_streak_date = end_of_current_streak_date
                        current_streak = 0

                except (ValueError, IndexError):
                    # 不正なデータ行は無視
                    continue
            
            # ファイルの最後にストリークが続いていた場合のチェック
            if current_streak > longest_streak:
                longest_streak = current_streak
                start_of_longest_streak_date = start_of_current_streak_date
                end_of_longest_streak_date = end_of_current_streak_date

        if longest_streak > 0:
            print(f"降水量が0だった最長連続日数: {longest_streak} 日間")
            print(f"期間: {start_of_longest_streak_date} から {end_of_longest_streak_date}")
        else:
            print("降水量データが見つからないか、常に降水がありました。")

    except FileNotFoundError:
        print(f"エラー: {file_path} が見つかりません。")
    except Exception as e:
        print(f"処理中にエラーが発生しました: {e}")

if __name__ == '__main__':
    find_longest_dry_spell()