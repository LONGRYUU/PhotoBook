import gensim
from gensim.models import Word2Vec
from gensim.scripts.glove2word2vec import glove2word2vec
import os
import csv
import nltk
from collections import Counter
import math
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
import torch
# from models import InferSent


stopwords = set(nltk.corpus.stopwords.words("english"))
stopwords.add('.')
model_path = 'D:\\WordEmbedding\\GoogleNews-vectors-negative300.bin'

def read_csv(path):
    freqs = {}
    with open(path) as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            freqs[row[0]] = int(row[1])

    return freqs

freqs_path = './data/freqs/doc_frequencies.tsv.txt'
doc_freqs = read_csv(freqs_path)
doc_freqs["NUM"] = 1288431
freqs = read_csv('./data/freqs/frequencies.tsv.txt')

class Sentence:
    def __init__(self, sentence):
        self.raw = sentence
        self.tokens = nltk.word_tokenize(sentence.lower().replace("’", "'").replace("‘", "'"))
        self.nonstop_tokens = [token for token in self.tokens if token not in stopwords]


def get_tokens(sentence, model, use_stoplist=True):
    tokens = sentence.nonstop_tokens if use_stoplist else sentence.tokens
    tokens = [token for token in tokens if token in model]
    return tokens


def tfidf(inputX, sentences, model ,use_stoplist=True):

    tokens_input = get_tokens(Sentence(inputX), model, use_stoplist)
    if tokens_input == 0:
        print("wrong input")
        return 0
    token_freqs_input = Counter(tokens_input)
    weights_input = [token_freqs_input[token] * math.log(doc_freqs["NUM"]/(doc_freqs.get(token, 0) + 1))
                     for token in token_freqs_input]
                     
    embedding_input = np.average([model[token] for token in token_freqs_input], axis=0, weights=weights_input).reshape(1, -1)

    sims = []
    for sentence in sentences:
        tokens = get_tokens(Sentence(sentence), model, use_stoplist)
        if len(tokens) == 0:
            sims.append(0)
            continue
        token_freqs = Counter(tokens)

        weights = [token_freqs[token] * math.log(doc_freqs["NUM"] / (doc_freqs.get(token, 0) + 1))
                   for token in token_freqs]
        embedding = np.average([model[token] for token in token_freqs], axis=0, weights=weights).reshape(1, -1)
        sim = cosine_similarity(embedding_input, embedding)
        sims.append(float(sim))
    return sims


def word_movers_distance(input, sentences, model, use_stoplist=True):
    sims = []
    tokens_input = get_tokens(Sentence(input), model, use_stoplist)
    if len(tokens_input) == 0:
        sims = np.zeros(len(sentences))
        return sims
    for sentence in sentences:
        tokens = get_tokens(Sentence(sentence), model, use_stoplist)

        if len(tokens) == 0:
            sims.append(0)
            continue
        sims.append(-model.wmdistance(tokens_input, tokens))
    return sims


def remove_first_principal_component(X):
    svd = TruncatedSVD(n_components=1, n_iter=7, random_state=0)
    svd.fit(X)
    pc = svd.components_
    XX = X - X.dot(pc.transpose()) * pc
    return XX


def sif(input, sentences, model, use_stoplist=False, a=0.001):
    
    total_freqs = sum(freqs.values())

    tokens_input = get_tokens(Sentence(input),model, use_stoplist=use_stoplist)
    weights_input = [a/(a + freqs.get(token, 0)/total_freqs) for token in tokens_input]
    embeding_input = np.average([model[token] for token in tokens_input], axis=0, weights=weights_input)

    embedings = []
    embedings.append(embeding_input)
    for sentence in sentences:
        tokens = get_tokens(Sentence(sentence), model, use_stoplist)
        weights = [a/(a + freqs.get(token, 0) / total_freqs) for token in tokens]
        embeding = np.average([model[token] for token in tokens], axis=0, weights=weights)
        embedings.append(embeding)

    remove_first_principal_component(np.array(embedings))
    sims = [cosine_similarity(embedings[0].reshape(1, -1), embedings[i].reshape(1, -1))[0][0]
            for i in range(1, len(embedings))]
    return sims



if __name__ == '__main__':

    a = 'a dog is drinking water'
    b = 'a cat is sleeping'
    model_path = 'E:\\WordEmbedding\\GoogleNews-vectors-negative300.bin'
    print('loading word2vec model')
    model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True, limit=100000)
    print('loaded')
    sims1 = tfidf(a, [b], model)
    print('using baseline:'+ str(sims1))
    sims1 = tfidf(b, [a], model)
    print('using baseline:'+ str(sims1))
    sims2 = word_movers_distance(a, [b], model)
    print('using wmd:'+ str(sims2))
    sims2 = word_movers_distance(b, [a], model)
    print('using wmd:'+ str(sims2))