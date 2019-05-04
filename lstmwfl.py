import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.optim as optim
import torch.nn.functional as F
import json
import csv
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score
from sklearn.metrics import classification_report

embedding_dim = 768
hidden_dim = 128
lr = 0.0001
class_num = 3
epoch = 30

def get_embedding(fname):
    res = []
    with open(fname, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            res.append(torch.FloatTensor(data['features'][0]['layers'][0]['values']))
    return res

def get_target(fname):
    res = []
    with open(fname, "r", encoding="utf-8") as f:
        r = csv.reader(f, delimiter='\t')
        for row in r:
            res.append(int(row[1]))
        '''
        for i in range(len(res)):
            if res[i] <= 2:
                res[i] = 1
            if res[i] == 3:
                res[i] = 2
        '''
    return torch.tensor(res)

# reference: https://github.com/marvis/pytorch-yolo2/blob/master/FocalLoss.py
class FocalLoss(nn.Module):
    def __init__(self, class_num, gamma=2):
        super(FocalLoss, self).__init__()
        self.alpha = Variable(torch.ones(class_num, 1))
        self.class_num = class_num
        self.gamma = gamma

    def forward(self, input, target):
        target = target - 1
        input = input[0]
        row = input.size(0)
        col = input.size(1)
        P = F.softmax(input)

        one_hot = input.data.new(row, col).fill_(0)
        one_hot = Variable(one_hot)
        index = target.view(-1, 1)
        one_hot.scatter_(1, index, 1.)

        probs = (P * one_hot).sum(1).view(-1, 1)

        log_p = probs.log()

        loss = -self.alpha * torch.pow((1 - probs), self.gamma) * log_p

        losss = loss.sum()

        return losss

class myLSTM(nn.Module):
    def __init__(self, embedding_dim, hidden_dim, class_num):
        super(myLSTM, self).__init__()
        self.lstm = nn.LSTM(embedding_dim, hidden_dim)
        self.fc = nn.Linear(hidden_dim, class_num)

    def forward(self, input):
        lstm_out, _ = self.lstm(input.view(1, 1, -1))
        logits = self.fc(lstm_out)
        return logits

def main():
    inputs = get_embedding("D:/TweetSA/train0.json")
    targets = get_target("train0.tsv")
    criterion = FocalLoss(class_num)
    model = myLSTM(embedding_dim, hidden_dim, class_num)
    optimizer = optim.Adam(model.parameters(), lr=lr)

    for e in range(epoch):
        for i in range(len(inputs)):
            #index = torch.tensor([targets[i] - 1])
            model.zero_grad()
            logits = model(inputs[i])
            #print(logits[0].size())
            #print(index.size())
            loss = criterion(logits, targets[i])
            loss.backward()
            optimizer.step()
            print("epoch: {0}-{1}  current loss: {2}".format(e, i, loss.item()))

    correct = 0
    pos = 0
    res = []
    with torch.no_grad():
        test = get_embedding("D:/TweetSA/dev0.json")
        labels = get_target("dev0.tsv")
        for i in range(len(test)):
            logits = model(test[i])
            logits = logits[0]
            probs = F.softmax(logits)
            _, pred = probs[0].max(0)
            pred += 1
            res.append(pred)

            if pred == labels[i].item():
                correct += 1
            if pred == 1 and labels[i] == 1:
                pos += 1
    lnum = labels.tolist().count(1)
    print("1 num: ", lnum)
    print("pos: ", pos)

    print("micro: ", f1_score(labels.tolist(), res, [1,2,3], average='micro'))
    print("macro: ", f1_score(labels.tolist(), res,[1,2,3], average='macro'))
    print("weighted: ", f1_score(labels.tolist(), res,[1,2,3], average='weighted'))
    print("accuracy: ", correct / len(labels))
    target_names = ['pos', 'neu', 'neg']
    print(classification_report(labels.tolist(), res, [1,2,3], target_names=target_names))

if __name__ == "__main__":
    main()