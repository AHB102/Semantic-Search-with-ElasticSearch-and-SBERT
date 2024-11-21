import streamlit as st
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
from math import ceil

Index = "products"
model = SentenceTransformer('all-mpnet-base-v2')
results_per_page = 5


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



def search(input):
    vector_input = model.encode(input)

    query = {
    "field" : "DescriptionVector",
    "query_vector":vector_input,
    "k":10,
    "num_candidates":500,
    }

    result = es.search(index="products",
                   body={
                   "knn" : query,
                    "_source" :["ProductName", "Description"]
                   } 
                   )
    
    res =  result["hits"]["hits"]
    return res


def main(): 
    st.write("# Simple semantic E commerce search")
    search_query = st.text_input("Search")

    if st.button("Search") and search_query:
        with st.spinner("Searching..."):
            results = search(search_query)
        st.subheader("Search results")

        # num_pages = ceil(len(results)/results_per_page)
        # page = st.slider("Page", 1, num_pages)

        # start_idx = (page - 1)*results_per_page
        # end_idx = start_idx + results_per_page

        for result in results:
            if "_source" in result:
                try:
                    st.header(f"{result['_source']['ProductName']}")
                except Exception as e :
                    print(e)

                try:
                    st.text(f"{result['_source']['Description']}")
                except Exception as e :
                    print(e)
                st.divider()

if __name__ == "__main__":
    main()
