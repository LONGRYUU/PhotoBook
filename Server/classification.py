import os
from collections import Counter
import similarityMethods as Sim
import torch
from stanfordcorenlp import StanfordCoreNLP
import numpy as np

def word_count(sentences, images, nlp):
    word_dict = {}
    for i, item in enumerate(sentences):
        # sentence = Sim.Sentence(item)
        tags = nlp.pos_tag(item)
        tokens = [pair[0] for pair in tags if pair[1] == 'NN']
        tokens = set(tokens)
        # tokens = sentence.nonstop_tokens if use_stop_list else sentence.tokens
        for token in tokens:
            if not str.isalnum(token):
                continue
            if token in word_dict:
                word_dict[token].append(images[i])
            else:
                word_dict[token] = []
                word_dict[token].append(images[i])
    
    return word_dict


def classifyByAttr(attrs, sentences, model, return_index=True):
    results = []
    if return_index:        
        for attr in attrs:
            sims = Sim.tfidf(attr, sentences, model)
            results.append(sims)
        results = np.array(results).T
        results = [(int(np.where(item == item.max())[0]), float(item.max())) if float(item.max()) > 0.4 else (-1, 0) for item in results]
    else:
        sims = Sim.sif(sentences[0], attrs, model)
        results = sims
    return results


if __name__ == '__main__':
    pass