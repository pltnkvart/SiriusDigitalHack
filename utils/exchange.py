import json


def exchange_words(path_to_file: str, column_name: str, word_being_changed: str, word_after_change: str, full_entry: bool = True) -> None:

    """
    Use this method to change entry of this word to new in appropriate column
    :param column_name: name of column where we will change words
    :param word_being_changed: word that will be changed
    :param word_after_change: witch word will be written after change
    :param full_entry: if true use == else use contains
    """

    with open(path_to_file, 'r') as file:

        data = json.load(file)
        for question_idx, question in enumerate(data):
            if question['question'] == column_name:
                for idx, answer in enumerate(question["answers"]):
                    need_to_exchange: bool = False
                    if full_entry:
                        if answer == word_being_changed:
                            question[idx] = word_after_change
                    else:
                        words = answer.split()
                        was_changed = False
                        for word_idx, word in enumerate(words):
                            if word.lower() == word_being_changed:
                                was_changed = True
                                words[word_idx] = word_after_change

                        if was_changed:
                            data[question_idx]["answers"][idx] = " ".join(words)
                            print(data[question_idx]["answers"][idx])

    with open(path_to_file, 'w', encoding='utf-8') as output_file:
        json.dump(data, output_file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    exchange_words("../datasets/results.json", "Комментарий к вопросу 2 Рассматриваете ли вы возможность остаться в компании/перевестись внутри отрасли? Были ли попытки руководителя сохранить вас в компании?", "да", "ага", full_entry=False)
