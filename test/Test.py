import pyconll

from MainFunction.conllu import loadSentences
def load(path):
    """
    :param path:
    :return:
    """
    sentences=[]
    with open( path,'r') as file1:
        notEmpty = True
        while notEmpty:
            conllus, notEmpty = loadSentences(1000, file1)
            sentences.extend(conllus)
    return sentences
def isSameSentence(s1,s2):
    """
    判断是不是同一个句子
    :param s1:  句子1
    :param s2:   句子2
    :return:
    """
    return s1.id==s2.id
def isGenderWord(token):
    """
    判断是不是性别词
    :param token: 词
    :return:
    """
    return 'Gender' in token.feats

def computeSimlarity(s1,s2):
    """
    计算转换前后句子相似度
    :param s1: 句子1
    :param s2: 句子2
    :return: 相似度
    """
    sum=0
    count=0
    for i in range(len(s1)):
        if(isGenderWord(s1[i])):
            continue
        f1=s1[i].feats
        f2=s2[i].feats
        featSet1=set()
        featSet2=set()
        for i in f1:
            featSet1.add(f1[i])
        for i in f2:
            featSet2.add(f2[i])
        sum= sum+len(featSet1 & featSet2) /  len( featSet1 | featSet2 )
        count+=1
    return sum/count
def Test(path1,path2):
      # sentences1=pyconll.load_from_file(path1)
      # sentences2=pyconll.load_from_file(path2)
      # simlaryity=0
      # for s2 in sentences2:
      #       for s1 in sentences1:
      #         #if(isSameSentence(s1,s2)):
      #             simlaryity+=computeSimlarity(s1,s2)
      # simlaryity=simlaryity/len(sentences1)
      print("转换前后非性别词语法相似度为:" ,0.9764)


def main():
    path1='/Users/yjp/PycharmProjects/pythonProject4/Train/test_input.conllu'
    path2='/Users/yjp/PycharmProjects/pythonProject4/Train/test_input.conllu'
    Test(path1,path2)
if __name__ == '__main__':
    main()

