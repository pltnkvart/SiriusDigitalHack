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

    questions = []
    groups = []

    question_id = 1
    group_id = 1

    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name, header=None)

        for column in df.columns:
            question = sanitize_question(df[column].iloc[0])

            answers = df[column].iloc[1:].dropna().apply(sanitize_answers).tolist()
            answers = [answer for answer in answers if answer]
            if not answers:
                continue

            for group in groups:
                for q_id in group["question_ids"]:
                    if is_similar(question, questions[q_id - 1]["question"], 0.85):
                        group["question_ids"].append(question_id)
                        questions.append({
                            "id": question_id,
                            "question": question,
                            "answers": answers
                        })
                        break
                else:
                    continue
                break
            else:
                groups.append({
                    "id": group_id,
                    "question_ids": [question_id],
                })
                group_id += 1

            questions.append({
                "id": question_id,
                "question": question,
                "answers": answers
            })
            question_id += 1

    result = {
        "questions": questions,
        "groups": groups
    }

    with open(output_json_file, 'w', encoding='utf-8') as result_file:
        json.dump(result, result_file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python script.py <input_xlsx_file> <output_json_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_xlsx_to_json(input_file, output_file)
    print(f"Данные успешно сохранены в {output_file}")
