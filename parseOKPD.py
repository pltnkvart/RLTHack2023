import openpyxl

file_path = 'okpd2_to_okpd.xlsx'

sheet_name = 'Лист1'

output_file = 'output.txt'

codes = ['26.20.1', '28.23', '28.24', '28.25', '28.11', '28.12', '28.13', '28.14', '28.15', '22.21', '22.22', '22.23', '26.51.4', '26.51.5', '26.51.8', '25.94', '27.11', '27.12']

workbook = openpyxl.load_workbook(file_path)

sheet = workbook[sheet_name]

with open(output_file, 'w', encoding='utf-8') as file:
    for row in sheet.iter_rows(values_only=True):
        code = row[0] 
        info = row[1]
        
        if (isinstance(code, str) and any(code.startswith(oneCode) for oneCode in codes) and
            isinstance(info, str)
        ):
            print(f"{code} {info}")
            file.write(f"{code}, {info}\n")

workbook.close()
