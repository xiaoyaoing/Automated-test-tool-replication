from sigmorphon_reinflection.data import LoadTFromColl, get_tags
from utils.ud import get_num_rel, get_num_upos
from pyconll import load_from_file


class Data:
    """
    T,pos,m
    """
    def __init__(self, train, dev, test):
        """
        Initializer
        :param train: file name of training set
        :param dev: file name of development set
        :param test: file name of test set
        """
        self.samples = []
        train_conll = load_from_file(train)
        dev_conll = load_from_file(dev)
        test_conll = load_from_file(test)
        self.train = LoadTFromColl(train_conll)
        self.dev = LoadTFromColl(dev_conll)
        self.test = LoadTFromColl(test_conll)
        self.tags = get_tags(self.train + self.dev + self.test)

        self._num_pos = get_num_upos()
        self._num_labels = get_num_rel()

    def num_tags(self):
        return len(self.tags)

    def num_pos(self):
        return self._num_pos

    def num_labels(self):
        return self._num_labels

    """
    Iterator
    """

    def __iter__(self):
        self.sample_id = 0
        return self

    def __next__(self):
        if self.sample_id < len(self.train):
            sample = self.train[self.sample_id]
            self.sample_id += 1
            return sample
        else:
            raise StopIteration
