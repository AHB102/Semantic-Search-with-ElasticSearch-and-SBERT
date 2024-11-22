from elasticsearch import Elasticsearch
from models.embeddings import EmbeddingModel

Index = "products"
model = EmbeddingModel()

try:
    es = Elasticsearch(
        "http://localhost:9200"
    )
except Exception as e:
    print(e)

if(es.ping()):
    print("Succcessfully connected to ElasticSearch")
else:
    print("Problem encountered during connection")
    
#Elasticsearch Search function
def search(input):
    vector_input = model.encode_text(input)

    query = {
    "field" : "DescriptionVector",
    "query_vector":vector_input,
    "k":10,
    "num_candidates":500,
    }

    result = es.search(index=Index,
                   body={
                   "knn" : query,
                    "_source" :["ProductName", "Description"]
                   } 
                   )
    
    res =  result["hits"]["hits"]
    return res