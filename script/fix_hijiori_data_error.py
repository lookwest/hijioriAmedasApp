import sys

def fix_csv_line(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"エラー: ファイル '{file_path}' が見つかりません。")
        return

    problematic_line_index = 17511  # 17512行目 (0-indexed)

    if len(lines) <= problematic_line_index:
        print("エラー: ファイルに行が不足しており、問題の行を修正できません。")
        return

    original_line = lines[problematic_line_index].strip()
    
    # この特定の不正な行をハードコードで修正
    expected_problematic_line = "2025/12/10,13,3.5,0,3,-3.4,6.6,西北西,西,0,5,23,,,,,,,,,,,2025/12/12025/12/11,23.0,7.0,2.3,11.6,-4.5,12.6 ,北西 ,西南西 ,5.6,7 ,21"

    # 行末の空白や改行を考慮して比較
    if original_line.strip() == expected_problematic_line.strip():
        # 正しい2行に置き換える
        line1 = "2025/12/10,13,3.5,0,3,-3.4,6.6,西北西,西,0,5,23,,,,,,,,,,,\n"
        line2 = "2025/12/11,23.0,7.0,2.3,11.6,-4.5,12.6,北西,西南西,5.6,7,21,,,,,,,,,,,\n"

        # 各行が23フィールドになるようにカンマを追加・調整
        line1_fields = line1.strip().split(',')
        line2_fields = line2.strip().split(',')

        corrected_line1 = ','.join(line1_fields[:23]) + '\n'
        corrected_line2 = ','.join(line2_fields[:23]) + '\n'
        
        lines[problematic_line_index] = corrected_line1
        lines.insert(problematic_line_index + 1, corrected_line2)

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"ファイル '{file_path}' の17512行目を修正しました。")
            print(f"  旧: {original_line}")
            print(f"  新1: {corrected_line1.strip()}")
            print(f"  新2: {corrected_line2.strip()}")
        except IOError:
            print(f"エラー: ファイル '{file_path}' に書き込めません。")

    else:
        print("17512行目は予期された問題の行と一致しませんでした。修正は行われませんでした。")
        print(f"実際の行: {original_line}")


if __name__ == "__main__":
    target_file = 'hijioriAmedas_data_utf8.csv'
    fix_csv_line(target_file)
