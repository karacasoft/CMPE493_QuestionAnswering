from find_related_sentence import find_related_sentence

from gensim.models import KeyedVectors 

wv_kw = KeyedVectors.load_word2vec_format('word2vec_tr.model', binary=True)

wv = {}

for word in wv_kw.index2word:
    wv[word] = wv_kw[word]
del wv_kw

import json
import pandas as pd
import tensorflow as tf
import numpy as np
from nltk import jaccard_distance

cfg = tf.ConfigProto()
cfg.gpu_options.per_process_gpu_memory_fraction = 0.6
cfg.gpu_options.allow_growth = True

tf.enable_eager_execution(config=cfg)

data = json.load(open("./data_dmnp_formatted.json"))[:100]
data_mapped = list(map(lambda x: { "C": find_related_sentence(x["Q"])[0], "Q": x["Q"], "A": x["A"] }, data))

vocab_df = pd.read_csv("./vocab.csv")
vocab = vocab_df["token"].values.tolist()
vocab_tensor = tf.convert_to_tensor(vocab)

wv_list = [ np.array(wv[w]) if w in wv else np.random.uniform(size=400) for w in vocab ]

word2idx = { x: i for i, x in enumerate(vocab) }

def find_word_id(word):
    _word = word.lower()
    while len(_word) > 5:
        if _word in word2idx:
            return word2idx[_word]
        else:
            _word = _word[:-1]
    word2idx[word] = len(vocab)
    vocab.append(word)
    wv_list.append(np.random.uniform(size=400))
    return word2idx[word]

def sentence_to_idx_array(sentence):
    return list(map(lambda x: find_word_id(x), sentence.split()))

def padding(x, size=10):
    if len(x) < size:
        x = x + (size - len(x)) * [0]
    return x

IDX_START = find_word_id("<start>")

data_mapped = list(map(lambda x: { "C": sentence_to_idx_array(x["C"]), "Q": sentence_to_idx_array(x["Q"]), "A": padding(sentence_to_idx_array(x["A"])) }, data_mapped))

wv_list = np.array(wv_list, dtype=np.float32)
assert len(wv_list) == len(vocab)





