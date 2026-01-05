

import csv
import os
import shutil

# --- 設定 ---
COPY_DEST_DIR = '/Users/ryu1hysk/Library/CloudStorage/OneDrive-個人用/amedas_data'
# --- 設定ここまで ---

def format_date_in_csv(file_path, dest_dir):
    """
    CSVファイルの日付形式をYYYY-MM-DDからYYYY/MM/DDに変換し、指定されたディレクトリにコピーします。
    """
    temp_file = file_path + '.tmp'
    try:
        with open(file_path, 'r', encoding='sjis', errors='ignore') as infile, \
             open(temp_file, 'w', encoding='sjis', newline='') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            for row in reader:
                if row:
                    # 日付部分のハイフンをスラッシュに置換
                    row[0] = row[0].replace('-', '/')
                writer.writerow(row)
        
        # 元のファイルを置き換える
        shutil.move(temp_file, file_path)
        print(f"'{file_path}' の日付フォーマットを YYYY/MM/DD に更新しました。")

        # コピー先にファイルをコピー
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        shutil.copy(file_path, os.path.join(dest_dir, os.path.basename(file_path)))
        print(f"{file_path} を {dest_dir} にコピーしました。")


    except FileNotFoundError:
        print(f"エラー: {file_path} が見つかりません。")
    except Exception as e:
        print(f"ファイルの処理中にエラーが発生しました: {e}")
        if os.path.exists(temp_file):
            os.remove(temp_file)

if __name__ == '__main__':
    format_date_in_csv('hijioriAmedas_data.csv', COPY_DEST_DIR)

