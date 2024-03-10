import math
from collections import Counter

import helper_functions
from helper_functions import *
helper = HelperFunctions()

pr_bucket_name = "bucket_ro"
normalize_doc = helper.read_pickle(pr_bucket_name, "normalize_dict/normalize_doc_dict.pkl")


class CosineSimilarity:
    def __init__(self):
        pass

    def q_normalize(self, q_counter):
        return 1 / math.sqrt(sum(count ** 2 for count in q_counter.values()))

    def get_top_n(self, sim_dict, N=3):
        """
        Sort and return the highest N documents according to the cosine similarity score.
        Generate a dictionary of cosine similarity scores
        """

        return sorted([(doc_id, round(score, 5)) for doc_id, score in sim_dict.items()], key=lambda x: x[1],
                      reverse=True)[:N]

    def calculate_similarity(self, search_q, idx, bucket_name, N=3):
        counter = Counter(helper.tokenize(search_q))
        get_pls = helper.get_posting_list(idx, list(counter.keys()), bucket_name)
        sim_dic = {}
        for token, p in get_pls:
            for doc_id, f in p:
                sim_dic[doc_id] = sim_dic.get(doc_id, 0) + counter[token] * f
        for d in sim_dic.keys():
            sim_dic[d] *= (self.q_normalize(counter)) * (normalize_doc[d])

        return self.get_top_n(sim_dic, N)

