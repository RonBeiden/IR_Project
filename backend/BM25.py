from helper_functions import *

helper = HelperFunctions()


class BM25_from_index:
    def __init__(self, index, bucket_name, k1=1.5, b=0.75):
        self.b = b
        self.k1 = k1
        self.index = index
        self.N = len(index.doc_len)
        self.AVGDL = sum(index.doc_len.values()) / self.N
        self.idf = {}
        self.bucket_name = bucket_name

    def calc_idf(self, list_of_tokens):
        idf = {}
        for term in list_of_tokens:
            if term in self.index.df.keys():
                n_ti = self.index.df[term]
                idf[term] = math.log(1 + (self.N - n_ti + 0.5) / (n_ti + 0.5))
            else:
                pass
        return idf

    def _score(self, query, doc_id, pls_dict):
        score = 0.0
        doc_len = self.index.doc_len[doc_id]
        for term in query:
            if term in self.index.df.keys(): # check??
                if doc_id in pls_dict[term].keys():
                    freq = pls_dict[term][doc_id]
                    numerator = self.idf[term] * freq * (self.k1 + 1)
                    denominator = freq + self.k1 * (1 - self.b + self.b * doc_len / self.AVGDL)
                    score += (numerator / denominator)
        return score

    def search(self, query, N=100):
        try:
            query_tokens = helper.tokenize(query)
            try:
                if len(query) < 25:
                    query = helper.similar_words(query_tokens, 0.7)
                else:
                    query = helper.similar_words_long(query_tokens)
            except:
                query = query_tokens

            idf = self.calc_idf(query)
            self.idf = idf

            d_pls = {}
            candidates = []

            for term in np.unique(query):
                if term in self.index.df.keys():
                    try:
                        curr_lst = self.index.read_a_posting_list("", term, self.bucket_name)
                        d_pls[term] = dict(curr_lst)

                        candidates += curr_lst
                    except:
                        pass

            candidates = set([x[0] for x in candidates])

            bm_25 = [(c, self._score(query, c, d_pls)) for c in candidates]
            bm_25 = sorted(bm_25, key=lambda x: x[1], reverse=True)[:N]

            return bm_25

        except:
            print(f'no mach for {query} in our search engine')
            pass
