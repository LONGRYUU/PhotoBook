import torch
import torchvision.models as models
import torch.nn as nn
from torch.autograd import Variable
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

class Encoder(nn.Module):
    def __init__(self, embed_size):
        super(Encoder, self).__init__()
        resnet = list(models.resnet152(pretrained=True).children())[:-1]
        self.cnn = nn.Sequential(*resnet)
        self.linear = nn.Linear(models.resnet152().fc.in_features, embed_size)
        self.bn = nn.BatchNorm1d(embed_size, momentum=0.01)
        self.init_weights()

    def init_weights(self):
        self.linear.weight.data.normal_(0.0, 0.02)
        self.linear.bias.data.fill_(0)

    def forward(self, images):
        featrues = self.cnn(images)
        featrues = Variable(featrues.data)
        featrues = featrues.view(featrues.size()[0], -1)
        featrues = self.bn(self.linear(featrues))
        return featrues

class Decoder(nn.Module):
    def __init__(self, embed_size, hidden_size, dict_size, num_layers):
        super(Decoder, self).__init__()
        self.embed = nn.Embedding(dict_size, embed_size)
        self.lstm = nn.LSTM(embed_size, hidden_size, num_layers, batch_first=True)
        self.linear = nn.Linear(hidden_size, dict_size)
        self.init_weight()

    def forward(self, features, captions, lengths):
        embeddings = self.embed(captions)
        embeddings = torch.cat((features.unsqueeze(1), embeddings), 1)
        embeddings = pack_padded_sequence(embeddings, lengths, batch_first=True)
        outputs,_ = self.lstm(embeddings)
        # print(outputs[0].size())
        outputs = self.linear(outputs[0])
        # print(outputs.size())
        return outputs

    def init_weight(self):
        self.embed.weight.data.uniform_(-0.1, 0.1)
        self.linear.weight.data.uniform_(-0.1, 0.1)
        self.linear.bias.data.fill_(0)
