import Levenshtein
import pandas as pd
import json
import sys
import re


def is_similar(text1, text2, threshold=0.6):
    text1 = text1.strip()
    text2 = text2.strip()

    if text1 in text2 or text2 in text1:
        return True

    if Levenshtein.ratio(text1, text2) >= threshold:
        return True

    set1 = set(text1.split())
    set2 = set(text2.split())
    if len(set1.intersection(set2)) / len(set1.union(set2)) >= threshold:
        return True

    # Other Methods
    return False


def sanitize_question(question: str) -> str:
    return question.strip()


def sanitize_answers(answers: str):
    if pd.isna(answers) or (isinstance(answers, str) and re.match(r'^(.)\1*$', answers.strip())):
        return None
    return answers.strip()


def convert_xlsx_to_json(input_xlsx_file: str, output_json_file: str):
    xls = pd.ExcelFile(input_xlsx_file)

    all_questions = []

    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name, header=None)

        for column in df.columns:
            question = sanitize_question(df[column].iloc[0])

            answers = df[column].iloc[1:].dropna().apply(sanitize_answers).tolist()
            answers = [answer for answer in answers if answer]

            for question_exists in all_questions:
                if is_similar(question, question_exists["question"], 0.85):
                    question_exists["answers"].extend(answers)
                    break
            else:
                if answers is not None:
                    question_data = {
                        "question": question,
                        "answers": answers
                    }
                    all_questions.append(question_data)

    with open(output_json_file, 'w', encoding='utf-8') as result_file:
        json.dump(all_questions, result_file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python script.py <input_xlsx_file> <output_json_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_xlsx_to_json(input_file, output_file)
    print(f"Данные успешно сохранены в {output_file}")
