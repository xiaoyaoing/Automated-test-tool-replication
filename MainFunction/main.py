# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import argparse
import contextlib
import os
import sys

from tqdm.contrib import DummyTqdmFile

print(sys.path)
sys.path.append('../')  #调整目录

import torch as torch
from tqdm import  tqdm
from MainFunction.MyModel import MyModel
from MainFunction.conllu import loadSentences
from  MainFunction.animate import  getAnimates
from sigmorphon_reinflection.decode import getDecodingModel



#
dir1 = os.path.dirname(__file__)
dir2 = os.path.dirname(dir1)
psi = dir2 + '/Trainedmodels/psi/spanish.pt'
reflect = dir2 + '/Trainedmodels/reinflection/spanish'

def getArgs():
    req=False
    parser = argparse.ArgumentParser()

    parser.add_argument('--in_files', required=req, help='Input conllu file',
                        default="/Users/yjp/nju/大三上/自动化测试/biasCDA/conllus/test_input.conllu")
    parser.add_argument('--out_file', required=req, help='Output conllu file',
                        default="/Users/yjp/nju/大三上/自动化测试/biasCDA/conllus/test_output2.conllu")
    parser.add_argument('--psi', required=False, help='Path to psi parameters',
                        default="/Users/yjp/PycharmProjects/pythonProject4/Trainedmodels/psi/spanish.pt")
    parser.add_argument('--reinflect', required=False, help='Path to reinflection model',
                        default="/Users/yjp/nju/大三上/自动化测试/biasCDA/models/reinflection/spanish")
    parser.add_argument('--animate_list', required=req, help='Path to animate noun list',
                        default="/Users/yjp/nju/大三上/自动化测试/biasCDA/animacy/spanish.tsv")
    return  parser.parse_args()

class Opt:

    def __init__(self,infile,outfile,model,animateList):
        self.in_files=infile
        self.out_file=outfile
        self.psi=model[0] if model!='none' else psi
        self.animate_list=animateList
        self.reinflect=reflect
def main():
    opt=getArgs()
    f(opt)
def f(opt):
    #return
    model = MyModel([0, 1, 2])
    psi = torch.load(opt.psi)
    print("Loading Models")
    with torch.no_grad():
        reinflectModel, device, decode_fn, decode_trg = getDecodingModel(opt.reinflect)
    file=opt.in_files
    part=1
    out = open(opt.out_file,"w")
    with open(file,"r") as f:
        not_empty=True
        print("Loading Sentences")

        while not_empty:
            print("Part",part)
            conll,not_empty=loadSentences(10000,f)
            sentenceConverseList=getAnimates(conll,opt.animate_list)
            print(len(sentenceConverseList),"种可能的转换被找到")
            #del conll

            print("转换句子ing～")
            convertedSentences=[]
            num=int(len(sentenceConverseList)/10)
            count=1
            for sentence in sentenceConverseList:
                if (count % num == 0):
                    str = "{}个句子已经被转换，一共{}个句子".format(count, len(sentenceConverseList))
                    print(str)
                count+=1
                converted=sentence.applyModel(model,psi,reinflectModel,device,decode_fn,decode_trg)
                convertedSentences.append(converted)
            print("{}个句子全部转换完毕！快去看看你的文件吧！".format(len(sentenceConverseList)))
            out.write("n\n".join(convertedSentences)+"\n\n")
            del sentenceConverseList
            part+=1

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    f=open()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
