import os

import json
from typing import List

import requests
from dotenv import load_dotenv

load_dotenv()


def analyze_word_frequency_gigachat(question: str, main_points: List[str]):

    authorization_token = os.getenv('AUTHORIZATION_TOKEN')
    giga_id = os.getenv('GIGA_ID')
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    payload = {
        'scope': 'GIGACHAT_API_PERS'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': f'{giga_id}',
        'Authorization': f'Basic {authorization_token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    access_token = json.loads(response.text)["access_token"]

    points = ' '.join(main_points)

    prompt = (
        f"На основе анализа частотных слов из ответов сотрудников на вопрос: {question}, объясните, почему сотрудники покидают компанию, и предложите решения для снижения числа увольнений. Вот список ключевых слов, которые встречались чаще всего: {points}. Проанализируйте эти данные и сделайте выводы."
        "\n\n1. Объясните основные причины увольнения сотрудников, опираясь на приведенные ключевые слова."
        "\n2. Какие факторы, исходя из этих данных, создают наибольшее напряжение среди сотрудников?"
        "\n3. Предложите конкретные шаги, которые компания может предпринять для уменьшения текучести кадров и улучшения условий работы, основываясь на выявленных причинах."
        "\n\nВаш ответ должен включать аналитическое объяснение каждой ключевой проблемы и предложить стратегические решения для их устранения."
    )

    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    payload = json.dumps({
        "model": "GigaChat",
        "messages": [
            {
                "role": "system",
                "content": "Ты профессиональный аналитик. Тебе необходимо проанализировать распределение по частоте ответов на вопрос. Выдай аналитику по предоставленным результатам."
            },
            {
                "role": "user",
                "content": f"{prompt}"
            }
        ],
        "stream": False,
        "update_interval": 0
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    if response.status_code == 200:
        response_data = response.json()
        return response_data['choices'][0]['message']['content'].strip()
    else:
        print(f"Ошибка при обращении к GigaChat API: {response.text}")
        return None
    

def get_word_frequency_gigachat(main_points: List[str]):
    authorization_token = os.getenv('AUTHORIZATION_TOKEN')
    giga_id = os.getenv('GIGA_ID')
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    payload = {
        'scope': 'GIGACHAT_API_PERS'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': f'{giga_id}',
        'Authorization': f'Basic {authorization_token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    access_token = json.loads(response.text)["access_token"]

    points = ' '.join(main_points)

    prompt = (
        f"Учитывая следующие слова: {points}, определите основную тему или идею, представленную этими словами.."
    )


    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    payload = json.dumps({
        "model": "GigaChat",
        "messages": [
            {
                "role": "system",
                "content": "Вы профессиональный анализатор тем. Ваша задача — определить центральную тему по заданным словам."

            },
            {
                "role": "user",
                "content": f"{prompt}"
            }
        ],
        "stream": False,
        "update_interval": 0
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    if response.status_code == 200:
        response_data = response.json()
        return response_data['choices'][0]['message']['content'].strip()
    else:
        print(f"Ошибка при обращении к GigaChat API: {response.text}")
        return None

if __name__ == '__main__':
    data = analyze_word_frequency_gigachat()
    print(data)
