# WikiSearch Engine

Welcome to our WikiSearch Engine, the culmination of our "Information Retrieval" course at BGU. Our aim was to create a powerful tool for searching English Wikipedia content efficiently. This search engine processes and indexes over six million documents, ensuring swift and accurate retrieval of relevant information from the vast corpus of Wikipedia articles. We've meticulously fine-tuned and optimized our techniques to deliver the best possible search experience for our users.

## Retrieval Methods

Our search engine employs a diverse range of retrieval methods, including:

- Inverted Index
- TF-IDF
- BM-25
- Word2vec
- Cosine Similarity
- Page Rank
- Page View

## Indexes

We have two main indexes:

- Index_Title
- Index_Body

## Capabilities

### Main Search Method

Our primary search method involves querying both the body and title indexes (with a 50:50 ratio) using the BM-25 scoring algorithm. We factor in page rank and page view metrics to rank the results effectively. Additionally, Word2Vec enhances result relevance.

### Additional Search Techniques

In addition to the main search method, our engine offers four other search techniques:

- **Search Body:** Retrieves information solely from Wikipedia page bodies using cosine similarity for comparison.
- **Search Title:** Retrieves information by focusing on Wikipedia page titles, prioritizing articles with more query terms in their title.
- **Get Page Rank:** Retrieves the PageRank score of a specific Wikipedia article identified by its unique ID.
- **Get Page View:** Retrieves the number of page views for a specific Wikipedia article identified by its unique ID.

## Notes

- Find our project on Google Cloud Storage [here](https://console.cloud.google.com/storage/browser/bucket_ro;tab=objects?forceOnBucketsSortingFiltering=true&hl=he&project=unique-cooler-407516&prefix=&forceOnObjectsSortingFiltering=false).
- You can access our search engine via the external IP address of our VM: [http://34.173.147.179:8080](http://34.173.147.179:8080) by activating it at `/search?query=YOUR_QUERY`.
- For any inquiries or assistance you may require, please feel free to reach out to us via email:

  Ron Beiden - [beiden@post.bgu.ac.il](mailto:beiden@post.bgu.ac.il)  
  Ori Flomin - [oriflo@post.bgu.ac.il](mailto:oriflo@post.bgu.ac.il)
