import requests
import time
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta
import os
import shutil

# --- 設定 ---
PREC_NO = '35'
BLOCK_NO = '1125' # 肘折の観測地点番号
CSV_FILE_PATH = 'hijioriAmedas_data_utf8.csv'
COPY_DEST_DIRS = [
    '/Users/ryu1hysk/Library/CloudStorage/OneDrive-個人用/amedas_data',
    '/Users/ryu1hysk/Library/Mobile Documents/com~apple~CloudDocs/Documents/amedas_data'
]
MAX_RETRIES = 3
RETRY_DELAY = 5 # 秒
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
# --- 設定ここまで ---

def get_last_date_from_csv():
    """CSVファイルから最後に記録された日付を取得する"""
    if not os.path.exists(CSV_FILE_PATH):
        print(f"エラー: {CSV_FILE_PATH} が見つかりません。")
        return None

    last_date_str = None
    try:
        with open(CSV_FILE_PATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in reversed(lines):
                if line.strip():
                    first_column = line.strip().split(',')[0]
                    try:
                        datetime.strptime(first_column, '%Y/%m/%d')
                        last_date_str = first_column
                        break
                    except ValueError:
                        continue
        
        if last_date_str:
            return datetime.strptime(last_date_str, '%Y/%m/%d')
        else:
            print("警告: CSVに有効な日付データが見つかりませんでした。")
            return None
    except Exception as e:
        print(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
        return None

def fetch_html_with_requests(url):
    """requestsを使ってURLからHTMLを取得する"""
    headers = {'User-Agent': USER_AGENT}
    for attempt in range(MAX_RETRIES):
        try:
            print(f"({attempt + 1}/{MAX_RETRIES}) requestsでHTMLを取得中...")
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status() # HTTPエラーがあれば例外を発生
            # 気象庁のサイトはShift_JISでエンコードされていることがあるため、正しくデコードする
            response.encoding = response.apparent_encoding
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"requestsの実行に失敗しました (Attempt {attempt + 1}/{MAX_RETRIES}): {e}")
            if attempt < MAX_RETRIES - 1:
                print(f"{RETRY_DELAY}秒後に再試行します...")
                time.sleep(RETRY_DELAY)
            else:
                print("最大リトライ回数に達しました。")
                return None
        except Exception as e:
            print(f"予期せぬエラーが発生しました: {e}")
            return None

def fetch_and_append_for_date(target_date):
    """指定された日付の気象データを取得し、CSVに追記する"""
    year, month, day = target_date.year, target_date.month, target_date.day
    url = f"http://www.data.jma.go.jp/stats/etrn/view/daily_a1.php?prec_no={PREC_NO}&block_no={BLOCK_NO}&year={year}&month={month}&day={day}&view="

    print(f"{year}/{month:02d}/{day:02d} のデータを取得中... (URL: {url}) ")

    html_content = fetch_html_with_requests(url)
    if not html_content:
        print(f"エラー: {year}/{month:02d}/{day:02d}のHTML取得に失敗しました。")
        return False

    try:
        # BeautifulSoupに渡す前にエンコーディングを指定する必要はない
        soup = BeautifulSoup(html_content, 'html.parser')
        data_table = soup.find('table', id='tablefix1')

        if not data_table:
            # HTMLの内容を少しだけ表示して、問題の診断に役立てる
            print(f"エラー: {year}/{month:02d}/{day:02d}のデータテーブルが見つかりませんでした。")
            print("取得したHTMLの先頭部分:", html_content[:200])
            return False

        rows = data_table.find_all('tr')
        new_row_data = None

        for row in rows[3:]:
            cells = row.find_all('td')
            if cells and len(cells) > 0:
                try:
                    day_from_cell = int(cells[0].text.strip())
                    if day_from_cell == day:
                        raw_data = [cell.text.strip().replace(')', '').replace(']', '') for cell in cells]
                        
                        def get_data(index):
                            return raw_data[index] if len(raw_data) > index and raw_data[index] else ''

                        new_row_data = [
                            f"{year}/{month:02d}/{day:02d}", get_data(1), get_data(2), get_data(4),
                            get_data(5), get_data(6), get_data(12), get_data(13),
                            get_data(14), get_data(15), get_data(16), get_data(17)
                        ]
                        break
                except (ValueError, IndexError):
                    continue
        
        if new_row_data:
            with open(CSV_FILE_PATH, 'a', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(new_row_data)
            print(f"-> {year}/{month:02d}/{day:02d} のデータを追記しました。")
            return True
        else:
            print(f"-> {year}/{month:02d}/{day:02d} のデータが見つかりませんでした。")
            return True

    except Exception as e:
        print(f"データの解析または書き込み中に予期せぬエラーが発生しました: {e}")
        return False

def main():
    """メイン処理"""
    last_date = get_last_date_from_csv()
    if last_date is None:
        print("処理を中断します。")
        return

    start_date = last_date + timedelta(days=1)
    end_date = datetime.now() - timedelta(days=1)

    print(f"最終記録日: {last_date.strftime('%Y/%m/%d')}")
    print(f"データ取得期間: {start_date.strftime('%Y/%m/%d')} から {end_date.strftime('%Y/%m/%d')}")

    if start_date > end_date:
        print("データは既に最新です。")
        return

    current_date = start_date
    while current_date <= end_date:
        if not fetch_and_append_for_date(current_date):
            print("回復不能なエラーのため、処理を中断します。")
            break
        time.sleep(1)
        current_date += timedelta(days=1)
    
    print("処理が完了しました。")

    # ファイルをコピー
    for dest_dir in COPY_DEST_DIRS:
        try:
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            shutil.copy(CSV_FILE_PATH, os.path.join(dest_dir, os.path.basename(CSV_FILE_PATH)))
            print(f"{CSV_FILE_PATH} を {dest_dir} にコピーしました。")
        except Exception as e:
            print(f"ファイルのコピー中にエラーが発生しました: {e}")

if __name__ == '__main__':
    main()