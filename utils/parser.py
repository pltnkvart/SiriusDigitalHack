import pandas as pd
import json
import sys


def convert_xlsx_to_json(input_xlsx_file: str, output_json_file: str):
    xls = pd.ExcelFile(input_xlsx_file)

    all_questions = []

    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name, header=None)

        for column in df.columns:
            question = df[column].iloc[0]
            answers = df[column].iloc[1:].dropna().tolist()
            question_data = {
                "question": question,
                "answers": answers
            }
            all_questions.append(question_data)

    with open(output_json_file, 'w', encoding='utf-8') as output_file:
        json.dump(all_questions, output_file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python script.py <input_xlsx_file> <output_json_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_xlsx_to_json(input_file, output_file)
    print(f"Данные успешно сохранены в {output_file}")
