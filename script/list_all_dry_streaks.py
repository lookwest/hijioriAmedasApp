import csv
from datetime import datetime

file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/hijioriAmedas_data_utf8.csv'

def find_all_dry_spells(top_n=10):
    """
    CSVファイルから降水量が0だったすべての連続期間を特定し、
    期間が長い順に上位 top_n 件を表示します。
    """
    streaks = []
    current_streak = 0
    start_of_current_streak_date = None
    end_of_current_streak_date = None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)  # ヘッダーをスキップ

            try:
                date_col_index = header.index('年月日')
                precip_col_index = header.index('降水量の合計(mm)')
            except ValueError as e:
                print(f"エラー: 必要な列が見つかりません - {e}")
                return

            for row in reader:
                try:
                    date_str = row[date_col_index]
                    datetime.strptime(date_str, '%Y/%m/%d') # 日付形式の検証

                    precipitation_str = row[precip_col_index].strip()
                    precipitation = float(precipitation_str) if precipitation_str else 0

                    if precipitation == 0:
                        if current_streak == 0:
                            start_of_current_streak_date = date_str
                        current_streak += 1
                        end_of_current_streak_date = date_str # 最終日を更新
                    else:
                        if current_streak > 0:
                            streaks.append({
                                "duration": current_streak,
                                "start": start_of_current_streak_date,
                                "end": end_of_current_streak_date
                            })
                        current_streak = 0

                except (ValueError, IndexError):
                    # 不正な行はスキップ
                    continue
            
            # ファイルの最後にストリークが続いていた場合のチェック
            if current_streak > 0:
                streaks.append({
                    "duration": current_streak,
                    "start": start_of_current_streak_date,
                    "end": end_of_current_streak_date
                })

        # 期間が長い順にソート
        sorted_streaks = sorted(streaks, key=lambda x: x['duration'], reverse=True)

        if sorted_streaks:
            print(f"降水量が0だった期間トップ{top_n}:")
            for i, streak in enumerate(sorted_streaks[:top_n]):
                print(f"{i+1}位: {streak['duration']} 日間 (期間: {streak['start']} から {streak['end']})")
        else:
            print("降水量データが見つからないか、常に降水がありました。")

    except FileNotFoundError:
        print(f"エラー: {file_path} が見つかりません。")
    except Exception as e:
        print(f"処理中にエラーが発生しました: {e}")

if __name__ == '__main__':
    find_all_dry_spells()