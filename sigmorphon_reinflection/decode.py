from functools import partial

import torch
from sigmorphon_reinflection.dataloader import BOS, EOS, UNK_IDX
from sigmorphon_reinflection.reinflection_model import decode_greedy


def getDecodingModel(model_file, max_len=100, beam_size=5, nonorm=False):
    with torch.no_grad():
        decode_fn = setup_inference_explicit( max_len, beam_size, nonorm)

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = torch.load(open(model_file, mode='rb'), map_location=device)
        model = model.to(device)

        trg_i2c = {i: c for c, i in model.trg_c2i.items()}
        decode_trg = lambda seq: [trg_i2c[i] for i in seq]

        return model, device, decode_fn, decode_trg
def setup_inference_explicit( max_len=100, beam_size=5, nonorm=False):
    decode_fn = partial(decode_greedy,max_len=max_len)
    return decode_fn
def decode_word(lemma, tags, model, device, decode_fn, decode_trg):
    src = encode(model, lemma, tags, device)
    pred, _ = decode_fn(model, src)
    return ''.join(decode_trg(pred))
def encode(model, lemma, tags, device):
    tag_shift = model.src_vocab_size - len(model.attr_c2i)

    src = []
    src.append(model.src_c2i[BOS])
    for char in lemma:
        src.append(model.src_c2i.get(char, UNK_IDX))
    src.append(model.src_c2i[EOS])

    attr = [0] * (len(model.attr_c2i) + 1)
    for tag in tags:
        if tag in model.attr_c2i:
            attr_idx = model.attr_c2i[tag] - tag_shift
        else:
            attr_idx = -1
        if attr[attr_idx] == 0:
            attr[attr_idx] = model.attr_c2i.get(tag, 0)

    return (torch.tensor(src, device=device).view(len(src), 1),
            torch.tensor(attr, device=device).view(1, len(attr)))