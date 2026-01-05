
import csv
import sys

# 標準出力のエンコーディングをUTF-8に設定
sys.stdout.reconfigure(encoding='utf-8')

file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/hijioriAmedas_data.csv'

try:
    with open(file_path, 'r', encoding='shift_jis') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
            header_col_count = len(header)
            print(f"ヘッダー行の列数は {header_col_count} です。")

            print("ヘッダーと列数が異なる行を検索しています...")
            found_mismatch = False
            for i, row in enumerate(reader, 2):  # 2行目から開始
                if len(row) != header_col_count:
                    print(f"  - 行番号: {i}, 列数: {len(row)}")
                    found_mismatch = True
            
            if not found_mismatch:
                print("列数が異なる行は見つかりませんでした。")

        except StopIteration:
            print("ファイルが空です。")
except FileNotFoundError:
    print(f"エラー: ファイルが見つかりません - {file_path}")
except Exception as e:
    print(f"エラーが発生しました: {e}")
