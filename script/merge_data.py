
import pandas as pd
import sys
import os

# --- 設定 ---
BASE_CSV_PATH = 'hijioriAmedas_data_utf8.csv'
NEW_CSV_PATH = 'downloaded_data.csv' # ユーザーがダウンロードしたファイル名
# ---

def merge_new_data():
    """
    ユーザーがダウンロードした新しい気象データ(CSV)を、
    既存の hijioriAmedas_data_utf8.csv にマージする。
    処理はすべて日本語の列名をベースに行う。
    """
    if not os.path.exists(NEW_CSV_PATH):
        print(f"エラー: 新しいデータファイル '{NEW_CSV_PATH}' が見つかりません。")
        print("気象庁のサイトからダウンロードしたCSVファイルを、このフォルダに置いてください。")
        sys.exit(1)

    print(f"'{BASE_CSV_PATH}' を読み込んでいます...")
    try:
        base_df = pd.read_csv(BASE_CSV_PATH, encoding='utf-8')
    except FileNotFoundError:
        print(f"エラー: 既存のデータファイル '{BASE_CSV_PATH}' が見つかりません。")
        sys.exit(1)
    except Exception as e:
        print(f"'{BASE_CSV_PATH}' の読み込み中にエラーが発生しました: {e}")
        sys.exit(1)

    print(f"新しいデータファイル '{NEW_CSV_PATH}' を読み込んでいます...")
    try:
        # 気象庁のCSVは最初の数行がヘッダー情報なので、データ本体が始まる行を探す
        # '年月日'というヘッダがある行をデータ開始行とする
        header_row_num = 0
        # ダウンロードしたファイルのエンコーディングはShift_JISと仮定
        with open(NEW_CSV_PATH, 'r', encoding='shift_jis') as f:
            for i, line in enumerate(f):
                if '年月日' in line:
                    header_row_num = i
                    break
        
        new_df = pd.read_csv(NEW_CSV_PATH, encoding='shift_jis', skiprows=header_row_num)

    except Exception as e:
        print(f"'{NEW_CSV_PATH}' の読み込み中にエラーが発生しました: {e}")
        print("ファイルの文字コードが Shift_JIS ではないか、形式が想定と異なる可能性があります。")
        sys.exit(1)
        
    # 日付列の型をdatetimeに統一
    base_df['年月日'] = pd.to_datetime(base_df['年月日'])
    new_df['年月日'] = pd.to_datetime(new_df['年月日'])

    print("データをマージしています...")
    # 既存のデータと新しいデータを結合
    # ignore_index=True で、インデックスを再採番する
    merged_df = pd.concat([base_df, new_df], ignore_index=True)
    
    print("重複データを削除し、ソートしています...")
    # '年月日'列で重複を削除 (新しいデータ、つまり後から結合した方を優先)
    merged_df = merged_df.drop_duplicates(subset='年月日', keep='last')
    
    # '年月日'列でソート
    merged_df = merged_df.sort_values(by='年月日')

    print(f"'{BASE_CSV_PATH}' を更新しています...")
    try:
        # 日付のフォーマットを YYYY/MM/DD に指定して保存
        merged_df.to_csv(BASE_CSV_PATH, index=False, date_format='%Y/%m/%d')
        print("データのマージが完了しました。")
        print(f"'{NEW_CSV_PATH}' は不要であれば手動で削除してください。")
    except Exception as e:
        print(f"'{BASE_CSV_PATH}' の書き込み中にエラーが発生しました: {e}")
        sys.exit(1)


if __name__ == '__main__':
    merge_new_data()
