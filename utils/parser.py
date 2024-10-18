import pandas as pd
import json
import sys


class EmployeeExitSurvey:
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


def convert_xlsx_to_json(input_xlsx_file: str, employee_json_file: str, hr_json_file: str):
    xls = pd.ExcelFile(input_xlsx_file)

    employee_responses = xls.parse("ответы сотрудников")
    hr_responses = xls.parse("ответы hr ")

    employee_exit_surveys = []
    for _, row in employee_responses.iterrows():
        employee_exit = EmployeeExitSurvey(
            reasons_leave=row['Комментарий к вопросу  1. Какие причины (факторы) сформировали ваше решение уйти из компании (выберите не более 3-х).'],
            additional_reasons=row['Комментарий к вопросу 1.1 Есть ли еще дополнительные причины, которые повлияли на ваше решение уйти из компании (выберите не более 3-х ).'],
            stay_option=row['Комментарий к вопросу 2 Рассматриваете ли вы возможность остаться в компании/перевестись внутри отрасли?'],
            return_option=row['Комментарий к вопросу 3 Рассматриваете ли вы возможность возвращения в компанию?'],
            recommend_company=row['Комментарий к вопросу 4 Готовы ли вы рекомендовать компанию как работодателя?']
        )
        employee_exit_surveys.append(employee_exit.__dict__)

    hr_exit_surveys = []
    for _, row in hr_responses.iterrows():
        hr_exit = HRExitSurvey(
            stay_option=row['Комментарий к вопросу 2 Рассматриваете ли вы возможность остаться в компании/перевестись внутри отрасли? Были ли попытки руководителя сохранить вас в компании?'],
            return_option=row['Комментарий к вопросу 3 Рассматриваете ли вы возможность возвращения в компанию, если нет, то почему?'],
            recommend_company=row['Комментарий к вопросу 4 Готовы ли вы рекомендовать компанию как работодателя, если нет, то почему?'],
            comment_on_change=row['Комментарий к ответу о причине увольнения "Желание сменить направление деятельности". Если сотрудник выбирает причину "Желание сменить направление деятельности, ему нужно прокомментировать эту причину.']
        )
        hr_exit_surveys.append(hr_exit.__dict__)

    with open(employee_json_file, 'w', encoding='utf-8') as employee_file:
        json.dump(employee_exit_surveys, employee_file, ensure_ascii=False, indent=2)

    with open(hr_json_file, 'w', encoding='utf-8') as hr_file:
        json.dump(hr_exit_surveys, hr_file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: python script.py <input_xlsx_file> <employee_json_file> <hr_json_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    employee_target_file = sys.argv[2]
    hr_target_file = sys.argv[3]

    convert_xlsx_to_json(input_file, employee_target_file, hr_target_file)
    print(f"Данные успешно сохранены в {employee_target_file} и {hr_target_file}")