import torch
import os
from model import Encoder, Decoder
from PIL import Image
from torchvision.transforms import transforms
import argparse
from pycocotools.coco import COCO
from global_vars import Dict
import pickle
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
import time


def greedy_search(features, decoder, dictionary):
    
    state = None
    caption = []

    for i in range(20):
        hidden, state = decoder.lstm(features, state)
        output = decoder.linear(hidden.squeeze(1))
        caption.append(output.max(1)[1])
        features = decoder.embed(output.max(1)[1])
        features = features.unsqueeze(1)
    
    caption = torch.stack(caption, 1)
    
    sentence = []
    
    for i in range(len(caption[0])):
        index = caption[0][i]
        if index == 2:
            break
        if index < 4:
            continue
        word = dictionary.get_word(int(index))
        if str.isalnum(word):
            sentence.append(word)
    return ' '.join(sentence)


def beam_search(features, decoder, dictionary, beam_size=5):
    
    length = beam_size

    state = None
    hidden,state = decoder.lstm(features, state)
    output = decoder.linear(hidden.squeeze(1))

    idx = output.max(1)[1]
    indices = [idx for i in range(beam_size)]
    scores = [0] * beam_size

    features = [decoder.embed(index).unsqueeze(1) for index in indices]
    
    state = [state] * beam_size
    hidden = [hidden] * beam_size
    caption = [[int(index)] for index in indices]
    stop = []
    weight = 1

    for i in range(19):

        # weight *= 0.8
        if len(stop) >= beam_size:
            break
        print('step:%d' % i)

        beam_size = len(features)

        indices = []
        # output = [1] * beam_size
        output = []

        for j in range(len(features)):
            # threads.append(BSThread(features, state, hidden, decoder, j, output, scores, weight))
            # threads[j].start()
            hidden[j],state[j] = decoder.lstm(features[j], state[j])
            output.append(decoder.linear(hidden[j].squeeze(1)).squeeze(0))
            # output[j] = output[j] * weight + scores[j]
            output[j] = output[j]

        # start = time.time()
        zipped = []
        # num = 0
        if i == 0:
            # zipped = [(item, j) for (j, item) in enumerate(output[0])]
            zipped = output[0]
        else:
            # outputs = torch.cat(output)
            # zipped = [(item, i) for (i, item) in enumerate(outputs)]
            zipped = torch.cat(output)

        # for j in range(num):
            # threads.append(SortThread(zipped[j]))
            # threads[j].start()

        # for j in range(num):
            # threads[j].join()
        
        # zipped = [res[j] for res in zipped for j in range(beam_size)]
        # zipped.sort(key=lambda x:x[0], reverse=True)
        locations = zipped.sort(descending=True)[1]

        # end = time.time()
        # print("time: %f" % (end - start))

        scores = []
        next_caption = []
        next_hidden = []
        next_state = []
        for j in range(beam_size):
            # pos = zipped[j][1]
            pos = locations[j]
            row = pos // len(output[0])
            col = pos % len(output[0])
            if col == 2:
                stop.append(caption[row])
            
            if col != 2:
                indices.append(col)
                # scores.append(zipped[j][0])
                # scores.append(float(zipped[pos]))
                next_caption.append(caption[row] + [col])
                next_hidden.append(hidden[row])
                next_state.append(state[row])

        caption = next_caption
        hidden = next_hidden
        state = next_state

        indices = torch.Tensor(indices).long()
        features = [decoder.embed(index.unsqueeze(0)).unsqueeze(1) for index in indices]

    sentences = []
    for item in stop:
        sentence = []
        for j in range(len(item)):
            pos = int(item[j])
            if pos == 2:
                break
            if pos < 4:
                continue
            word = dictionary.get_word(pos)
            if str.isalnum(word):
                sentence.append(word)
        s = ' '.join(sentence)
        if s not in sentences:
            sentences.append(s)


    for i in range(length - len(stop)):
        sentence = []
        for j in range(len(caption[i])):
            pos = int(caption[i][j])
            if pos == 2:
                break
            if pos < 4:
                continue
            word = dictionary.get_word(pos)
            if str.isalnum(word):
                sentence.append(word)
        s = ' '.join(sentence)
        if s not in sentences:
            sentences.append(' '.join(sentence))

    return sentences
    

def infer(encoder, decoder, dictionary, transform, image_path, search=greedy_search):
    image = Image.open(image_path).convert('RGB')
    img = transform(image)
    features = encoder(img.unsqueeze(0))
    # state = None
    # caption = []
    features = features.unsqueeze(1)

    return search(features, decoder, dictionary)
