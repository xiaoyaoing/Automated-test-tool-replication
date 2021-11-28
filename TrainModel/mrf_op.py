import torch
from torch.autograd import Function
import torch.nn as nn
from MainFunction.MyModel import MyModel as Model


class MRF(Function):
    """
    Class to compute dpsi of a given sentence
    """
    def __init__(self, model, sentence):
        super(MRF, self).__init__()
        self.sentence = sentence
        self.model = model

    def forward(self, psi):
        """
        :param psi: psi potentials to use in computing -log Pr(T|m)
        :return: -log Pr(T|m)
        """
        self.save_for_backward(psi)
        val = -self.model.log_prob(self.sentence.T, self.sentence.pos, self.sentence.m, psi)
        return torch.Tensor([val])

    def backward(self, grad_output):
        """
        :param grad_output: N/A
        :return: gradient of -log Pr(T|m) wrt psi
        """
        psi = self.saved_tensors[0]
        dpsi = -self.model.dlog_prob(self.sentence.T, self.sentence.pos, self.sentence.m, psi)
        del psi
        return dpsi



class MRF_Lin(torch.nn.Module):
    """
    Class to initialize belief propagation model with linear parametrization of psi
    """
    def __init__(self, tags, sentence=None):
        super(MRF_Lin, self).__init__()
        self.model = Model(tags)
        self.sentence = sentence

    def forward(self, psi):
        """
        :param psi: psi parameters
        :return: application of model to current sentence
        """
        return MRF(self.model, self.sentence)(psi)
