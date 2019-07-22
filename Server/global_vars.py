from flask_sqlalchemy import SQLAlchemy
import gensim
from stanfordcorenlp import StanfordCoreNLP
from model import Encoder, Decoder
import pickle
import torch
import os
from torchvision.transforms import transforms
from build_dict import Dict

db = SQLAlchemy()


model_path = 'E:\\WordEmbedding\\GoogleNews-vectors-negative300.bin'
nlp_path = 'D:\\stanford-corenlp-full-2018-10-05'
dictionary_path = 'E:\\COCO\\dict\\dict.pkl'

transform = transforms.Compose([transforms.RandomCrop(224),
                                    transforms.RandomHorizontalFlip(),
                                    transforms.ToTensor(),
                                    transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))])

dictionary = {'value':None}

encoder = Encoder(256)
decoder = Decoder(256, 512, 11560, 1)
print('loading caption model')
encoder.load_state_dict(torch.load(os.path.join('E:\\COCO\\params', 'encoder-0-70000')))
decoder.load_state_dict(torch.load(os.path.join('E:\\COCO\\params', 'decoder-0-70000')))
print('caption model loaded')
encoder.eval()
decoder.eval()
print('loading word embedding model')
model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True, limit=100000)
print('word embedding model loaded')
nlp = StanfordCoreNLP(nlp_path)