from helper_functions import *

# import helper class
helper = HelperFunctions()
pr_bucket_name = "bucket_ro"

##### pagerank & pageview #####
pagerank = helper.read_pickle(pr_bucket_name, "page_rank/pagerank_dict.pkl")
pageview = helper.read_pickle(pr_bucket_name, "page_view/pageview.pkl")
pagerank = {entry['id']: entry['pagerank'] for entry in pagerank}


class Rankers:
    def page_rank_helper(self, wiki_ids):
        res = []
        for doc_id in wiki_ids:
            try:
                res.append(pagerank[doc_id])
            except:
                res.append(0)
        return res

    def page_view_helper(self, lst):
        res = []
        for doc_id in lst:
            try:
                res.append(pageview[doc_id])
            except:
                res.append(0)
        return res
