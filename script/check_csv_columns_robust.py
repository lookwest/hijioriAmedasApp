
import sys

# 標準出力のエンコーディングをUTF-8に設定
sys.stdout.reconfigure(encoding='utf-8')

file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/hijioriAmedas_data.csv'

try:
    with open(file_path, 'r', encoding='shift_jis') as f:
        lines = f.readlines()
        if not lines:
            print("ファイルが空です。")
            exit()

        header_col_count = lines[0].count(',')
        print(f"ヘッダー行のカンマの数は {header_col_count} です (列数は {header_col_count + 1})。")

        print("ヘッダーとカンマの数が異なる行を検索しています...")
        found_mismatch = False
        for i, line in enumerate(lines[1:], 2):  # 2行目から開始
            col_count = line.count(',')
            if col_count != header_col_count:
                print(f"  - 行番号: {i}, カンマの数: {col_count} (列数: {col_count + 1})")
                found_mismatch = True
        
        if not found_mismatch:
            print("カンマの数が異なる行は見つかりませんでした。")

except FileNotFoundError:
    print(f"エラー: ファイルが見つかりません - {file_path}")
except Exception as e:
    print(f"エラーが発生しました: {e}")
