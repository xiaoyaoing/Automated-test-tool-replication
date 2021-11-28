from sigmorphon_reinflection.data import LoadTFromSentence
from  utils.reinflection import get_feats,get_lines
from sigmorphon_reinflection.decode import  decode_word
class MySentenceConverse:
    def __init__(self,sentence,changes):
        self.sentence=sentence
        self.changes=changes
    def applyModel(self,model,psi,reflectModel,device,decode_fn,decode_trg):
        """
        应用模型到句子转换上 选择最优的转换策略
        :param model:
        :param psi:
        :param reinflecion_model:
        :param device:
        :param decode_fn:
        :param decode_trg:
        :return:
        """
        t=LoadTFromSentence(self.sentence)
        phi=model.createPhi(t)
        toFix=[]
        for change in self.changes:
            toFix.append((change[0],(lambda  x:2 if x else 1)(change[-1])))
        bestTags = model.selectBestSequence(t.T, t.pos, psi, phi, toFix)
        originTags=t.m
        changeId=[change[0] -1  for change in self.changes]
        tagsToChange=[]
        for i in range(0,len(originTags)):
            origintag=originTags[i]
            bestTag=bestTags[i]
            if origintag!=0 and origintag!=bestTag and i not in changeId:
                tagsToChange.append(i)
        sentence=self.changeSentenceForm(tagsToChange, reflectModel, device, decode_fn, decode_trg)
        return sentence
    def changeSentenceForm(self, tagsToChange, reflectModel, device, decode_fn, decode_trg):
        """
        根据要修改的tagId改变句子中的词的形式
        :param tagsToChange:  要修改的tagId
        :param reflectModel:
        :param device:
        :param decode_fn:
        :param decode_trg:
        :return:
        """
        lines=[]
        if self.sentence.id:
            changeId=""
            for change in self.changes:
                changeId="-"+str(change[0])+"-"+("M" if change[-1] else "F")
            lines.append("#sent_id = "+self.sentence.id+changeId)
        changeIds=[change[0]-1 for change in self.changes]
        for i in range(len(self.sentence)):
            token=self.sentence[i]
            line=token.conll()
            if not token.is_multiword() and int(token.id) - 1 in tagsToChange + changeIds:
                if token.lemma and len(token.feats["Gender"]) == 1:
                    line = self._change_line(token,reflectModel, device, decode_fn, decode_trg)
            lines.append(line)
        return "\n".join(lines)

    def _change_line(self, token, reflectModel, device, decode_fn, decode_trg):
        """

        :param token:
        :param reflectModel:
        :param device:
        :param decode_fn:
        :param decode_trg:
        :return:
        """
        is_masc = token.feats['Gender'].pop() == 'Masc'
        token.feats['Gender'].add('Fem' if is_masc else 'Masc')
        line = token.conll()
        parts = line.split("\t")
        for change in self.changes:
            if int(token.id) == change[0]:
                parts[2] = change[1]
        tags = get_feats(token)
        new_form = decode_word(token.lemma, tags, reflectModel, device, decode_fn, decode_trg)
        parts[1] = new_form
        return "\t".join(parts)

    def change_forms(self, form_idxs, reinflection_model, device, decode_fn, decode_trg):
        """
        Change the forms of a selection of words in the sentence using a reinflection model

        :param form_idxs: word indices to change
        :param reinflection_model: reinflection model
        :param device: device related to reinflection model
        :param decode_fn: Decoding function
        :param decode_trg: Decoding target
        :return: UD style string of new sentence
        """
        lines = []
        if self.sentence.id:
            change_id = ""
            for change in self.changes:
                change_id += "-" + str(change[0]) + "-" + ("M" if change[-1] else "F")
            lines.append("# sent_id = " + self.sentence.id + change_id)
        change_ids = [change[0] - 1 for change in self.changes]
        for i in range(len(self.sentence)):
            token = self.sentence[i]
            line = token.conll()
            if not token.is_multiword() and int(token.id) - 1 in form_idxs + change_ids:
                if token.lemma and len(token.feats["Gender"]) == 1:
                    line = self._change_line(token, reinflection_model, device, decode_fn, decode_trg)
            lines.append(line)
        return "\n".join(lines)

