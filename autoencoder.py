import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
import torch.nn.functional as F
import json
import torch
import csv

class autoencoder(nn.Module):
    def __init__(self):
        super(autoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(768, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 12),
            nn.ReLU(),
            nn.Linear(12, 3),
        )
        self.decoder = nn.Sequential(
            nn.Linear(3, 12),
            nn.ReLU(),
            nn.Linear(12, 64),
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, 768),
            nn.Tanh()
        )

    def forward(self, x):
        latent = self.encoder(x)
        x_hat = self.decoder(latent)
        return x_hat

def get_embedding(fname, label=None):
    res = []
    row = 0
    labelfname = fname.split(".")[0].split("/")[-1] + ".tsv"
    with open(labelfname, "r", encoding="utf-8") as file:
        r = csv.reader(file, delimiter='\t')
        r = list(r)
        with open(fname, "r", encoding="utf-8") as f:
            for line in f:
                if label is not None:
                    if label != r[row][1]:
                        row += 1
                        continue
                row += 1
                data = json.loads(line)
                l = [0] * len(data['features'][0]['layers'][0]['values'])
                for i in range(len(l)):
                    for word in data['features']:
                        if word['token'] != '[CLS]' or word['token'] != '[SEP]':
                            l[i] += (word['layers'][0]['values'][i] / (len(data['features']) - 2))
                res.append(torch.FloatTensor(l))

    return res

if __name__ == "__main__":
    lr = 1e-4
    num_epochs = 10
    model = autoencoder().cuda()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-5)
    tensor_lst = get_embedding("D:/TweetSA/train0.json", "3")
    test = get_embedding("D:/TweetSA/dev0.json")

    neg = []
    for epoch in range(num_epochs):
        count = 0
        for x in tensor_lst:
            #Variable.cuda()
            count += 1
            data = Variable(x).cuda()
            # ===================forward=====================
            output = model(data)
            loss = criterion(output, data)
            # ===================backward====================
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        # ===================log========================
            print("epoch: {0}, data: {1}, loss: {2}".format(epoch, count, loss.item()))
            if epoch == 9:
                neg.append(loss)

    print("pos data in")
    pos = []
    with torch.no_grad():
        count = 0
        for x in test:
            # Variable.cuda()
            count += 1
            data = Variable(x).cuda()
            # ===================forward=====================
            output = model(data)
            loss = criterion(output, data)
            print("pos data: {0}, loss: {1}".format(count, loss.item()))
            pos.append(loss)
