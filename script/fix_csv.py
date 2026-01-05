
import sys

def fix_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    problematic_line_index = 17512  # 0-based index
    if len(lines) > problematic_line_index:
        line = lines[problematic_line_index]
        if '2025/12/12' in line:
            # Find the starting position of the second date
            date2_start_pos = line.find('2025/12/12')
            
            # Split the line into two
            line1 = line[:date2_start_pos]
            line2 = line[date2_start_pos:]
            
            # Replace the problematic line with the two corrected lines
            lines[problematic_line_index] = line1 + '\n'
            lines.insert(problematic_line_index + 1, line2)

            # Write the corrected lines back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print("CSV file has been fixed.")
        else:
            print("The problematic line does not contain the expected second date.")
    else:
        print("The file does not have enough lines to contain the problematic line.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        fix_csv(file_path)
    else:
        print("Please provide the file path as a command-line argument.")
