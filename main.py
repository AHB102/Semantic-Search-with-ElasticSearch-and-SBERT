import streamlit as st
from elasticsearch import Elasticsearch
from app.search import search
from models.embeddings import EmbeddingModel

model = EmbeddingModel()

def main(): 
    st.write("# Simple semantic E commerce search")
    search_query = st.text_input("Search")

    if st.button("Search") and search_query:
        with st.spinner("Searching..."):
            results = search(search_query)
        st.subheader("Search results")

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