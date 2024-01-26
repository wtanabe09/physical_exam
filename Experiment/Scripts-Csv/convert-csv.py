import csv

def convert_csv_to_int(input_csv, output_csv):
    with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            print(row)
            # for cell in row:
            # 各要素を浮動小数点数から整数に変換
            int_row = [int(float(cell)*1000) for cell in row]
            writer.writerow(int_row)

if __name__ == "__main__":
    input_csv_path = '2_a_20231103103438865789_edit1.csv'  # 入力CSVファイルのパス
    output_csv_path = '2_a_20231103103438865789_edit1-1.csv'  # 出力CSVファイルのパス

    convert_csv_to_int(input_csv_path, output_csv_path)

# float_number = 5.21134495735168E-01
# integer_number = int(float_number * 100)

# print(integer_number)