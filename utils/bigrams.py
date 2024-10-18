import nltk
from nltk import bigrams
from nltk.corpus import stopwords
from collections import Counter
import pymorphy2
import re
import pickle

# Предварительно загрузим токенизатор NLTK
nltk.download('punkt')
nltk.download('stopwords')

# Инициализация морфологического анализатора
morph = pymorphy2.MorphAnalyzer()

stop_words = stopwords.words('russian')
custom_stop_words = ["например", "также"]
stop_words.extend(custom_stop_words)

# Функция для предобработки текста и лемматизации
def preprocess_text(text):
    # Приведение текста к нижнему регистру
    text = text.lower()
    # Удаление всех символов кроме букв и пробелов
    text = re.sub(r'[^а-яё ]', ' ', text)
    # Токенизация (разбиение на слова)
    words = nltk.word_tokenize(text)

    stop_words = set(stopwords.words('russian'))
    filtered_tokens = [word for word in words if word not in stop_words]

    # Лемматизация каждого слова
    lemmatized_words = [morph.parse(word)[0].normal_form for word in filtered_tokens]
    return lemmatized_words

with open('answers.pickle', 'rb') as handle:
    answers = pickle.load(handle)

with open('cluster_labes.pickle', 'rb') as handle:
    cluster_labels = pickle.load(handle)

res = []
for cluster_idx in range(max(cluster_labels)):
    appropriate_answers = [answers[answer_idx] for answer_idx, cluster_value in enumerate(cluster_labels) if cluster_value == cluster_idx]
    res.append(appropriate_answers)
    print(f"for cluster idx: {cluster_idx}, len is: {len(res[-1])}")



# Пример предложений
sentences = [
    "Мама мыла раму.",
    "Папа чистил машину.",
    "Мама готовила ужин.",
    "Папа читал книгу."
]
for cluster_idx, cluster_sentences in enumerate(res):
    
    print(cluster_idx, cluster_sentences)

    sentences = cluster_sentences
    # Предобработка и создание биграмм для каждого предложения
    all_bigrams = []
    for sentence in sentences:
        words = preprocess_text(sentence)
        all_bigrams.extend(list(bigrams(words)))

    # Подсчет частот биграмм
    bigram_freq = Counter(all_bigrams)

    # Вывод самых частотных биграмм
    most_common_bigrams = bigram_freq.most_common(10)
    print(f"for cluster {cluster_idx}")
    for bigram, freq in most_common_bigrams:
        print(f"Биграмма: {bigram}, Частота: {freq}")
