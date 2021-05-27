import sys
sys.path.append('D:\Projects\All Projects\Text-Author-Identification-using-Naive-Bayes')

from author_identifier.util import utils
from author_identifier.model.nb_model import model
from collections import Counter, defaultdict
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import pickle

data = pd.read_csv("../../data/train.csv")

Rogers_text = data[data.Speaker == "Captain America"]
Rogers_text = " ".join([str(x) for x in list(Rogers_text["Dialogue"])])

Stark_text = data[data.Speaker == "Iron Man"]
Stark_text = " ".join([str(x) for x in list(Stark_text["Dialogue"])])

# Tokenize the dialogues
all_tokens = utils.tokenize(Rogers_text) + utils.tokenize(Stark_text)

# Create vocabulary
vocab = defaultdict(lambda : {})

for item in set(all_tokens):
    vocab[item]["Stark"] = 0
    vocab[item]["Rogers"] = 0

stark_counts = Counter(utils.tokenize(Stark_text))
rogers_counts = Counter(utils.tokenize(Rogers_text))

for item in stark_counts:
    vocab[item]["Stark"] = stark_counts[item]
    vocab[item]["Rogers"] = rogers_counts[item]

vocab_items = len(vocab)
stark_vocab_count = sum([stark_counts[x] for x in stark_counts])
rogers_vocab_count = sum(rogers_counts[x] for x in rogers_counts)

# Prior Probability Estimation
prob_rogers = len(data[data.Speaker == "Captain America"]) / len(data)
prob_stark  = len(data[data.Speaker == "Iron Man"]) / len(data)
log_prior = np.log(prob_stark / prob_rogers)

# Conditional Probability computation with laplacian smoothing
probabilities = defaultdict(utils.defdict)
for item in vocab:
    probabilities[item]["Stark"] = (vocab[item]["Stark"] + 1) / (stark_vocab_count + vocab_items)
    probabilities[item]["Rogers"] = (vocab[item]["Rogers"] + 1) / (rogers_vocab_count + vocab_items)
    probabilities[item]["lambda"] = np.log(probabilities[item]["Stark"] / probabilities[item]["Rogers"])

probabilities["xxunk"]["Stark"] = (0 + 1) / (stark_vocab_count + vocab_items)
probabilities["xxunk"]["Rogers"] = (0 + 1) / (rogers_vocab_count + vocab_items)
probabilities["xxunk"]["lambda"] = np.log(probabilities["xxunk"]["Stark"] / probabilities["xxunk"]["Rogers"])

# Save the conditional probabilities and log_prior values
model_artifact = {"probabilites": probabilities,
                  "log_prior": log_prior}

with open("model_artifact.pkl", "wb") as f:
    pickle.dump(model_artifact, f)
    f.close()

# Infer on train dataset
predictions = []
for sentence in data.Dialogue:
    predictions.append(model.predict(str(sentence), probabilities, log_prior))

print(accuracy_score([x[0] for x in predictions], data.Speaker))

# Infer on test dataset (i.e. script of Avengers: Endgame)
test_data = pd.read_csv("test.csv")
predictions = []
for sentence in test_data.Dialogue:
    predictions.append(model.predict(str(sentence), probabilities, log_prior))

print(accuracy_score([x[0] for x in predictions], test_data.Speaker))