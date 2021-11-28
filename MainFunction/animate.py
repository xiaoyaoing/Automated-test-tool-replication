from copy import deepcopy
from itertools import combinations
from tqdm import  tqdm
from MainFunction.MySentenceConverse import MySentenceConverse



def converseToFemal(mascWord,words):
    """
    converse a  masc word to femaml
    :param mascWord: 待转换的阳性词
    :param words: 英文单词-阴性词-阳性词的三元组组成的列表
    :return: 阳性词的阴性形式
    """
    MascNum=int(len(words)/2)
    for i in range(MascNum,MascNum*2):
        if(mascWord==words[i]):
            return words[i-MascNum]
    raise ValueError(mascWord)
def converseToMale(femWord,words):
    """
    与上一函数类似
    :param femWord:
    :param words:
    :return:
    """
    femNum = int(len(words) / 2)
    list1=words[0:femNum]
    list2=words[femNum:]
    for i in range(0, femNum):
        if (femWord == words[i]):
            return words[i + femNum]
    raise ValueError(femWord)
def getAnimates(conllu,animateF):
    """
    :param conllu: conllu对象
    :param animateList:  存储animate的文件
    :return: 返回可能的性别词变换排列
    """
    help=[]
    with open(animateF, "r") as f:
        lines = f.readlines()
    lines = [line.strip().split("\t") for line in lines]
    words = [line[1] for line in lines] + [line[2] for line in lines]
    sentenceConverseList=[]
    num=int(len(conllu)/10)
    count=1
    for sentence in conllu:
        if(count%num==0):
            str="{}个句子已经被查找，一共{}个句子".format(count,len(conllu))
            print(str)
        count+=1
        changes=[]
        for token in sentence:
            if  'Gender' not in token.feats or len(token.feats['Gender'])!=1 or token.upos !="NOUN":
                continue
            masc=next(iter(token.feats['Gender'])) == 'Masc'
            if token.lemma in words:
                try:
                    if masc:
                        convertedWord=converseToFemal(token.lemma,words)
                    else:
                        convertedWord=converseToMale(token.lemma,words)
                except ValueError:
                    continue
                changes.append([int(token.id),convertedWord,not masc])
        changesList=[]
        help.extend(changes)
        for i in range(1,len(changes)+1):
            changesList.extend(combinations(changes,i)) #组合多种可能的变化情况

        for change in changesList:
            sentenceConverseList.append(MySentenceConverse(deepcopy(sentence),change))
    return  sentenceConverseList

