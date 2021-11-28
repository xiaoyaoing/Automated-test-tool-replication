import torch
import torch.nn as nn
import torch.optim as optim
import torch.autograd as autograd
from TrainModel.mrf_op import  MRF_Lin
from TrainModel.Data import Data
import os
from tqdm import tqdm



class NeuralMRF(nn.Module):
    """ neural MRF """

    def __init__(self, data, out_dir, linear, use_v1, hack_v2):
        super(NeuralMRF, self).__init__()
        self.data = Data(data + "/-train.conllu", data + "/-dev.conllu", data + "/-test_input.conllu")
        self.num_pos = self.data.num_pos()
        self.num_labels = self.data.num_labels()
        self.num_tags = self.data.num_tags()
        self.out_dir = out_dir
        self.linear = linear
        self.mrf = MRF_Lin(self.data.tags)
        self.register_parameter('psi', None)
        self.psi = nn.Parameter(
            torch.randn(self.num_pos, self.num_pos, self.num_labels, self.num_tags, self.num_tags,
                        dtype=torch.float64))
    def forward(self, sentence):
        """ computation of the log-likelihood with pytorch """
        self.mrf.sentence = sentence
        return self.mrf(self.psi)
    def fit(self, epochs=100, precision=1e-5):
        self.optimizer = optim.Adam(self.parameters(), lr=0.001, weight_decay=0.001)

        def step():
            """ step in the optimization """
            train_loss = dev_loss = 0
            print("  Optimizing parameters on training data loss")
            count=1
            num=int(len(self.data.train)/100)
            for sentence in self.data:
            #for sentence in tqdm(self.data, total=len(self.data.train)):
                if(count%num==0):
                    print("{} of {}已经完成".format(count,len(self.data.train)))
                count+=1
                self.optimizer.zero_grad()
                loss = self.forward(sentence)
                train_loss += loss
                loss.backward()
                self.optimizer.step()
                del loss
            print("  Calculating dev loss")
            num=int(len(self.data.dev)/100)
            count=1
            for sentence in self.data.dev:
            #for sentence in tqdm(self.data.dev, total=len(self.data.dev)):
                if (count % num == 0):
                    print("{} of {}已经完成".format(count, len(self.data.train)))
                count += 1
                dev_loss += self.forward(sentence)
            return train_loss / len(self.data.train), dev_loss / len(self.data.dev)
        for i in range(epochs):
            print("Computing epoch", i + 1, "...")
            # Do optimization step
            train_loss, dev_loss = step()
            # Save current parameters
            file = os.path.join(self.out_dir, "psi_" +
                                str(round(train_loss[0].item(), 6)) + "_" +
                                str(round(dev_loss[0].item(), 6)) + "_epoch" + str(i + 1) + ".pt")
            torch.save(self.psi, file)


            print("Completed epoch", i + 1)
            print("    Training loss:", train_loss[0].item())
            print("    Dev loss:     ", dev_loss[0].item())
            if i > 0 and prev_loss - train_loss < precision:
                break
            prev_loss = train_loss

def TrainInterface(data,out):
    nmrf=NeuralMRF(data,out,True,False,False)
    nmrf.fit()

if __name__ == "__main__":
    from argparse import ArgumentParser

    #调试用改了一下默认的data和outdir
    p = ArgumentParser()
    p.add_argument('--data', required=False, type=str,
                   default="/Users/yjp/PycharmProjects/pythonProject4/Train/")
    p.add_argument('--out_dir', required=False, type=str,
                   default="/Users/yjp/PycharmProjects/pythonProject4/Train/")
    p.add_argument('--use_v1', default=False, action='store_true')
    p.add_argument('--hack_v2', default=False, action='store_true')
    p.add_argument('--linear', default=True, action='store_true')

    args = p.parse_args()

    nmrf = NeuralMRF(args.data, args.out_dir, args.linear, args.use_v1, args.hack_v2)
    nmrf.fit()
