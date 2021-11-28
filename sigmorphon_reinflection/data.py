from utils.ud import get_rel_id, get_upos_id, get_gender_id


class SentenceT:
    """
    表示句子的依赖结构的类
    """
    def __init__(self,T, pos, m_o, m_m=None, i=None, from_masc=None, sent_id=None):
        self.T = T
        self.pos = pos
        self.m = m_o
        self.m_eval = m_m
        self.i = i
        self.from_masc = from_masc
        self.eval_sent = True if i else False
        self.sent_id = sent_id
def LoadTFromSentence(sentence):
    T=[]
    pos=[]
    m=[]
    for token in sentence:
        try:
            index = int(token.id)
        except ValueError:
            continue
        deprel=token.deprel
        upos=token.upos
        head=token.head
        T.append((index,int(token.head),get_rel_id(deprel)))
        pos.append(get_upos_id(upos))
        feats=token.feats
        if('Gender' not in feats or (feats['Gender']!={"Masc"} and feats['Gender']!={"Fem"})):
            tag=0
        else:
            tag=get_gender_id(next(iter(feats['Gender'])))
        m.append(tag)
    return SentenceT(T,pos,m)

def LoadTFromColl(conll):
    """
        Get dependency trees and tag vectors from a collection of sentences
        :param conll: collection of UD parsed sentences
        :return: samples
        """
    samples = []
    for sent in conll:
        samples.append(LoadTFromSentence(sent))
    return samples



def get_tags(samples):
    """
    :param samples: samples used for training
    :return: all the tags that occur in samples
    """
    tags = []
    for sentence in samples:
        for t in sentence.m:
            if t not in tags:
                tags.append(t)
    tags.sort()
    return tags