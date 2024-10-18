import pandas as pd
import json
import sys

class WorkerExitSurvey:
    def __init__(self, reasons_leave, additional_reasons, stay_option, return_option, recommend_company):
        self.reasons_leave = reasons_leave
        self.additional_reasons = additional_reasons
        self.stay_option = stay_option
        self.return_option = return_option
        self.recommend_company = recommend_company


class HRExitSurvey:
    def __init__(self, stay_option, return_option, recommend_company, comment_on_change):
        self.stay_option = stay_option
        self.return_option = return_option
        self.recommend_company = recommend_company
        self.comment_on_change = comment_on_change


def convert_xlsx_to_json(input_xlsx_file: str, worker_json_file: str, hr_json_file: str):
    xls = pd.ExcelFile(input_xlsx_file)

    employee_responses = xls.parse("ответы сотрудников")
    hr_responses = xls.parse("ответы hr ")

    worker_exit_surveys = []
    for _, row in employee_responses.iterrows():
        worker_exit = WorkerExitSurvey(
            reasons_leave=row['Комментарий к вопросу  1. Какие причины (факторы) сформировали ваше решение уйти из компании (выберите не более 3-х).'],
            additional_reasons=row['Комментарий к вопросу 1.1 Есть ли еще дополнительные причины, которые повлияли на ваше решение уйти из компании (выберите не более 3-х ).'],
            stay_option=row['Комментарий к вопросу 2 Рассматриваете ли вы возможность остаться в компании/перевестись внутри отрасли?'],
            return_option=row['Комментарий к вопросу 3 Рассматриваете ли вы возможность возвращения в компанию?'],
            recommend_company=row['Комментарий к вопросу 4 Готовы ли вы рекомендовать компанию как работодателя?']
        )
        worker_exit_surveys.append(worker_exit.__dict__)

    hr_exit_surveys = []
    for _, row in hr_responses.iterrows():
        hr_exit = HRExitSurvey(
            stay_option=row['Комментарий к вопросу 2 Рассматриваете ли вы возможность остаться в компании/перевестись внутри отрасли? Были ли попытки руководителя сохранить вас в компании?'],
            return_option=row['Комментарий к вопросу 3 Рассматриваете ли вы возможность возвращения в компанию, если нет, то почему?'],
            recommend_company=row['Комментарий к вопросу 4 Готовы ли вы рекомендовать компанию как работодателя, если нет, то почему?'],
            comment_on_change=row['Комментарий к ответу о причине увольнения "Желание сменить направление деятельности". Если сотрудник выбирает причину "Желание сменить направление деятельности, ему нужно прокомментировать эту причину.']
        )
        hr_exit_surveys.append(hr_exit.__dict__)

    with open(worker_json_file, 'w', encoding='utf-8') as worker_file:
        json.dump(worker_exit_surveys, worker_file, ensure_ascii=False, indent=2)

    with open(hr_json_file, 'w', encoding='utf-8') as hr_file:
        json.dump(hr_exit_surveys, hr_file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: python script.py <input_xlsx_file> <worker_json_file> <hr_json_file>")
        sys.exit(1)

    input_xlsx_file = sys.argv[1]
    worker_json_file = sys.argv[2]
    hr_json_file = sys.argv[3]

    convert_xlsx_to_json(input_xlsx_file, worker_json_file, hr_json_file)
    print(f"Данные успешно сохранены в {worker_json_file} и {hr_json_file}")
