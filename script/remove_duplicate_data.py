
import pandas as pd

file_path = '/Users/ryu1hysk/gemini_code/hijiori_AMEDAS/hijioriAmedas_data.csv'

def remove_duplicate_entries():
    """
    CSVファイルから重複する日付のデータを削除します。
    """
    try:
        # Shift-JISでCSVを読み込む
        # ヘッダーがないため、header=Noneを指定し、最初の行をデータとして読み込む
        df = pd.read_csv(file_path, encoding='sjis', header=None, on_bad_lines='skip')
        
        # カラム名を指定（日付が最初のカラムであることを前提）
        # 実際のカラム名ではなく、処理のために一時的に名前を割り当てる
        df.columns = [
            '日付', '降水量の合計(mm)', '1時間降水量の最大(mm)', 
            '平均気温(℃)', '最高気温(℃)', '最低気温(℃)', 
            '最大風速(m/s)', '最大風速の風向', '最大瞬間風速(m/s)', 
            '最大瞬間風速の風向', '最深積雪(cm)', '積雪深合計(cm)'
        ]

        # 日付をdatetimeオブジェクトに変換
        df['日付'] = pd.to_datetime(df['日付'], errors='coerce')
        
        # 無効な日付を含む行を削除
        df.dropna(subset=['日付'], inplace=True)

        # 日付でソートし、重複する日付の最後の行を残す（最新のデータが残るように）
        df.sort_values(by='日付', inplace=True)
        df.drop_duplicates(subset=['日付'], keep='last', inplace=True)

        # クリーンアップしたデータを元のCSVファイルに上書き保存
        # ヘッダーは出力しない
        df.to_csv(file_path, encoding='sjis', header=False, index=False)
        print(f"{file_path} から重複するデータを削除しました。")

    except FileNotFoundError:
        print(f"エラー: {file_path} が見つかりません。")
    except Exception as e:
        print(f"処理中にエラーが発生しました: {e}")

if __name__ == '__main__':
    remove_duplicate_entries()
