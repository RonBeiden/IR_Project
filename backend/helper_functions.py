# imports
import concurrent
import sys
from collections import Counter, OrderedDict
import itertools
from itertools import islice, count, groupby

import google
import pandas as pd
import os
import re
from operator import itemgetter
import nltk
from nltk.stem.porter import *
from nltk.corpus import stopwords
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from time import time
from timeit import timeit
from pathlib import Path
import pickle
import numpy as np
from google.cloud import storage
import itertools
import math
from inverted_index_gcp import *
from contextlib import closing
from collections import Counter
import gensim.models
import gensim.downloader as api
import gc

##### corpus stopwords #####
nltk.download('stopwords')
english_stopwords = frozenset(stopwords.words('english'))
corpus_stopwords = ["category", "references", "also", "external", "links",
                    "may", "first", "see", "history", "people", "one", "two",
                    "part", "thumb", "including", "second", "following",
                    "many", "however", "would", "became"]

RE_WORD = re.compile(r"""[\#\@\w](['\-]?\w){2,24}""", re.UNICODE)
all_stopwords = english_stopwords.union(corpus_stopwords)


model_glove_wiki = api.load("glove-wiki-gigaword-300")


class HelperFunctions:
    def __init__(self):
        pass

    def read_pickle(self, bucket_name, pickle_route):
        client = storage.Client()
        blob = client.bucket(bucket_name).blob(pickle_route)
        pick = pickle.loads(blob.download_as_string())
        return pick

    ##### tokenizer ######

    def tokenize(self, text):
        """
        This function aims in tokenize a text into a list of tokens. Moreover, it filter stopwords.

        Parameters:
        -----------
        text: string , represting the text to tokenize.

        Returns:
        -----------
        list of tokens (e.g., list of tokens).
        """
        list_of_tokens = [token.group() for token in RE_WORD.finditer(text.lower()) if
                          token.group() not in all_stopwords]
        return list_of_tokens

    TUPLE_SIZE = 6
    TF_MASK = 2 ** 16 - 1  # Masking the 16 low bits of an integer

    def get_posting_list(self, idx, query, bucket_name):
        posting_lists = []
        for token in query:
            try:
                p = idx.read_a_posting_list("", token, bucket_name)
            except:
                print('couldnt use reader in get pl')
                p = []
            posting_lists.append((token, p))
        return posting_lists

    def similar_words(self, tokens, ecc):
        global model_glove_wiki
        candidates = model_glove_wiki.most_similar(positive=tokens, topn=4)
        res = [word for word, similarity in candidates if similarity > ecc]
        for tok in res:
            tokens += self.tokenize(tok)
        return tokens[:5]

    def similar_words_long(self, tokens):
        global model_glove_wiki
        sim_w = []
        res = []

        for token in tokens:
            candidates = model_glove_wiki.most_similar(positive=token, topn=1)
            res += [(similarity, word) for word, similarity in candidates if similarity > 0.7]

        sim_w += tokens
        for sim, tok in sorted(res, reverse=True):
            if len(sim_w) < 5:
                sim_w += self.tokenize(tok)
            else:
                break
        return sim_w


