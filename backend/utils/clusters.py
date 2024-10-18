from typing import List, Tuple

import nltk
import numpy as np
from sklearn.cluster import AffinityPropagation
from transformers import BertTokenizer, BertModel
import torch
import json

from nltk import bigrams
from nltk.corpus import stopwords
from collections import Counter
import pymorphy2
import re

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')


def make_clusterization(input_json_path: str) -> List[List[Tuple[List[Tuple[str, int]], int]]]:
    def preprocess_text(text: str) -> List[str]:
        text = text.lower()
        text = re.sub(r'[^а-яё ]', ' ', text)
        print(f"-----> {text} <------")
        words = nltk.word_tokenize(text, language='russian')

        stop_words = set(stopwords.words('russian'))
        filtered_tokens = [word for word in words if word not in stop_words]
        lemmatized_words = [morph.parse(word)[0].normal_form for word in filtered_tokens]

        return lemmatized_words

    def find_bigrams(input_clusters: List[List[List[str]]]) -> List[List[Tuple[List[Tuple[str, int]], int]]]:
        output_bigrams = []
        for question_idx, answers_list in enumerate(input_clusters):
            bigrams_list = []
            for cluster_idx, cluster_sentences in enumerate(answers_list):
                all_bigrams = []
                for sentence in cluster_sentences:
                    print(f"sentence - {sentence}")
                    words = preprocess_text(sentence)
                    all_bigrams.extend(list(bigrams(words)))

                bigram_freq = Counter(all_bigrams)
                most_common_bigrams = bigram_freq.most_common(3)
                bigrams_list.append((most_common_bigrams, len(cluster_sentences)))
            output_bigrams.append(bigrams_list)

        return output_bigrams

    def find_clusters(this_question: str, answers: List[str]) -> List[List[str]]:
        question_tokens = tokenizer(this_question, return_tensors='pt', padding='max_length', max_length=128, truncation=True)

        with torch.no_grad():
            # todo: make lemma and remove stop words
            question_embedding = model(**question_tokens).last_hidden_state.mean(dim=1).numpy()

        answer_embeddings = []

        for answer in answers:
            answer_tokens = tokenizer(answer, return_tensors='pt', padding='max_length', max_length=128, truncation=True)

            with torch.no_grad():
                # todo: make lemma and remove stop words
                answer_embedding = model(**answer_tokens).last_hidden_state.mean(dim=1).numpy()
            joint_embedding = np.concatenate((question_embedding, answer_embedding), axis=1)
            answer_embeddings.append(joint_embedding)

        X = np.array(answer_embeddings).reshape(len(answers), -1)

        sk_ap = AffinityPropagation()
        cluster_labels = sk_ap.fit_predict(X)
        split_answers: List[List[str]] = []

        for cluster_idx in range(max(cluster_labels)):
            appropriate_answers = [answers[answer_idx] for answer_idx, cluster_value in enumerate(cluster_labels) if
                                   cluster_value == cluster_idx]
            split_answers.append(appropriate_answers)
            # print(f"for cluster idx: {cluster_idx}, len is: {len(res[-1])}")

        return split_answers

    with open(input_json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')

    morph = pymorphy2.MorphAnalyzer()

    output_clusters = []
    for question in data:
        question_clusters = find_clusters(question['question'], question['answers'])
        output_clusters.append(question_clusters)
        print(question_clusters)

    found_bigrams = find_bigrams(output_clusters)

    return found_bigrams
