import os
from pycocotools.coco import COCO
import argparse
import nltk
import pickle
from collections import Counter


class Dict(object):
    def __init__(self):
        self.word2id = {}
        self.id2word = {}
        self.counter = 0

    def __len__(self):
        return len(self.word2id)

    def __call__(self, word):
        if word not in self.word2id:
            return self.word2id['<unk>']
        return self.word2id[word]

    def add_word(self, word):
        if word not in self.word2id:
            self.word2id[word] = self.counter
            self.id2word[self.counter] = word
            self.counter += 1

    def get_word(self, index):
        if index >= len(self.id2word):
            return ['<unk>']
        return self.id2word[index]


def build_dict(json, threshold):
    coco = COCO(json)
    ids = coco.anns.keys()
    counter = Counter()
    dictionary = Dict()
    dictionary.add_word('<pad>')
    dictionary.add_word('<beg>')
    dictionary.add_word('<end>')
    dictionary.add_word('<unk>')

    for i, index in enumerate(ids):
        caption = str(coco.anns[index]['caption'])
        tokens = nltk.tokenize.word_tokenize(caption.lower())
        counter.update(tokens)

    for word, cnt in counter.items():
        if cnt >= threshold:
            dictionary.add_word(word)

    print(len(dictionary))
    return dictionary


def save_dict(dictionary, path):
    with open(path, 'wb') as f:
        pickle.dump(dictionary, f)


def main(args):
    dictionary = build_dict(json=args.caption_path, threshold=args.threshold)
    save_dict(dictionary, args.dict_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dict_path', type=str, default='D:\\COCO\\dict\\dict.pkl')
    parser.add_argument('--threshold', type=int, default=4)
    parser.add_argument('--caption_path', type=str, default='D:\\COCO\\annotations\\captions_train2017.json')
    main(parser.parse_args())
