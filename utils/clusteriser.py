import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import AffinityPropagation
from sklearn.metrics import euclidean_distances, adjusted_rand_score
from transformers import BertTokenizer, BertModel
import torch
import pandas
from sklearn.decomposition import PCA
import json


def load_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    questions = data[0]["question"]
    all_answers = data[0]["answers"]
    
    return questions, all_answers



# Example question and answers
#question = "What would you do during a picnic?"
#answers = [
#    "Eat burger", "Drink a beer", "Play football", "Play soccer",
#    "Enjoy a root beer", "Swallow a steak", "Eat a salad", "Something else"
#]

question_all, answers_all = load_data("datasets/results.json")

question = question_all
answers = answers_all

print(question)
print(len(answers))

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Tokenize and generate embeddings for the question
question_tokens = tokenizer(question, return_tensors='pt', padding='max_length', max_length=128, truncation=True)

print(question_tokens)

with torch.no_grad():
    question_embedding = model(**question_tokens).last_hidden_state.mean(dim=1).numpy()

# Tokenize and generate embeddings for answers and concatenate with question embedding
answer_embeddings = []
for i, answer in enumerate(answers):
    
    print(i)

    answer_tokens = tokenizer(answer, return_tensors='pt', padding='max_length', max_length=128, truncation=True)
    with torch.no_grad():
        answer_embedding = model(**answer_tokens).last_hidden_state.mean(dim=1).numpy()
    joint_embedding = np.concatenate((question_embedding, answer_embedding), axis=1)
    answer_embeddings.append(joint_embedding)

X = np.array(answer_embeddings).reshape(len(answers), -1)

sk_ap = AffinityPropagation()
cluster_labels = sk_ap.fit_predict(X)


#for i, answer in enumerate(answers):
#    print(f"Answer: {answer} | Cluster: {cluster_labels[i]}")
print(cluster_labels)
print(max(cluster_labels))

df =pandas.DataFrame(X, columns = [f"dim_{x}" for x in range(X.shape[1])])
pca= PCA(n_components=2).fit(df)
X2D = pca.transform(df)


plt.style.use("seaborn-v0_8-whitegrid")
plt.scatter(X2D[:, 0], X2D[:, 1], c=cluster_labels, cmap='rainbow', s=10)
#for i, answer in enumerate(answers):
#    plt.text(X2D[i][0] + i*.1, X2D[i][1] + i*.05, answer, fontsize=8, ha='right', va='bottom')
plt.title(f"{question}")

plt.show()