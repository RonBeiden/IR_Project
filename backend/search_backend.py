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
from contextlib import closing
from collections import Counter
import gensim.models
import gensim.downloader as api
import gc
from BM25 import *
from helper_functions import *
from inverted_index_gcp import *
from helper_rankers import *

# import helper class
helper = HelperFunctions()
ranker = Rankers()
pagerank = pagerank
pageview = pageview

pr_bucket_name = "bucket_ro"
inverted_title = helper.read_pickle(pr_bucket_name, "title_index/title_index.pkl")
inverted_body = helper.read_pickle(pr_bucket_name, "text_index/text_index.pkl")
doc_id_to_title_dic = helper.read_pickle(pr_bucket_name, "title_id_dict_6m/doc_id_to_title_dict_6m.pkl")


class FinalSearch:
    def __init__(self):
        ##### Set Wights #####
        self.title_weight = 0.5
        self.text_weight = 0.5
        self.bm_weight = 0.5
        self.page_view_weight = 0.25
        self.page_rank_weight = 0.25

    def title_string(self, doc_id):
        """
        returns the document title given its doc id
        """
        title = doc_id_to_title_dic.get(doc_id)
        return title if title else "Couldn't find matching title"

    def merge_results(self, title_scores, body_scores, title_w=0.5, text_w=0.5):
        """
        This function merge and sort documents retrieved by its weighte score (e.g., title and body).
         """

        temp_dict = defaultdict(float)
        for doc_id, score in title_scores:
            temp_dict[doc_id] += title_w * score
        for doc_id, score in body_scores:
            temp_dict[doc_id] += text_w * score

        return temp_dict


    def merge_bm25_scores(self, query):
        """
        find the best bm25 docs and scores for the query.
        using title and body index
        """
        bm25_title = BM25_from_index(inverted_title, pr_bucket_name)
        bm25_body = BM25_from_index(inverted_body, pr_bucket_name)

        try:
            title_score = bm25_title.search(query, N=50)
            body_score = bm25_body.search(query, N=50)
            BM25_score = self.merge_results(title_score, body_score, self.title_weight, self.text_weight)
            # BM25_score = merge_results(title_score, body_score, t_s, b_s)
            return BM25_score
        except:
            print('An error occurred while searching')
            pass


    def merge_bm25_pr_pv(self, bm25_dic):
        """
        calculate the final score using bm25, page view, page rank.
        """
        try:
            max_bm25 = max(bm25_dic.values())
        except:
            print('Error in BM25')
            return

        max_pr = max(ranker.page_rank_helper(bm25_dic.keys()))
        max_pv = max(ranker.page_view_helper(bm25_dic.keys()))

        for key, val in bm25_dic.items():
            bm = val
            page_rank = pagerank.get(key, 0)
            page_view = pageview.get(key, 0)
            bm25_dic[key] = (bm * self.bm_weight / max_bm25) + (page_rank * self.page_rank_weight / max_pr) + \
                            (page_view * self.page_view_weight / max_pv)
        return bm25_dic

    def search_helper(self, query):
        try:
            bm_25 = self.merge_bm25_scores(query)
            calc_scores = self.merge_bm25_pr_pv(bm_25)
            sort_res = list(sorted(calc_scores.items(), key=lambda x: x[1], reverse=True)[:10])
            res = [(str(doc_id), self.title_string(doc_id)) for doc_id, acc in sort_res]

            #gc.collect()
            return list(res)

        except Exception as e:
            print(f'Error is - {e}')
            return []



