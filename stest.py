import streamlit as st
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
from datetime import datetime
from collections import Counter
import json
import os
import threading

# Elasticsearch Index Name
INDEX_NAME = "products"

# Thread-safe logging mechanism
class ThreadSafeFileWriter:
    _lock = threading.Lock()

    @classmethod
    def write_log(cls, filename, log_entry):
        """Thread-safe method to write logs."""
        with cls._lock:
            try:
                with open(filename, "a") as log_file:
                    log_file.write(json.dumps(log_entry) + "\n")
            except Exception as e:
                st.error(f"Error logging interaction: {e}")

# Load SBERT Model Once
@st.cache_resource
def load_model():
    return SentenceTransformer('all-mpnet-base-v2')
model = load_model()

# Elasticsearch Initialization
@st.cache_resource
def get_elasticsearch_connection():
    try:
        es = Elasticsearch("http://localhost:9200")
        if es.ping():
            print("Successfully connected to Elasticsearch")
            return es
        else:
            print("Problem encountered during connection")
            return None
    except Exception as e:
        print(e)
        return None
es = get_elasticsearch_connection()

# Interaction Tracking
INTERACTION_THRESHOLD = 5
LOGS_FILE = "user_logs.json"

# Utility Functions
def encode_query(input):
    """Encodes the input query using the SBERT model."""
    return model.encode(input)

def search(input_query):
    """Performs a semantic search on Elasticsearch."""
    vector_input = encode_query(input_query)

    query = {
        "field": "DescriptionVector",
        "query_vector": vector_input,
        "k": 10,
        "num_candidates": 500,
    }

    result = es.search(index=INDEX_NAME, body={
        "knn": query,
        "_source": ["ProductName", "Description"]
    })

    return result["hits"]["hits"]

def log_interaction(search_query, clicked_product=None):
    """Logs user interaction to a file."""
    log_entry = {
        "search_query": search_query,
        "clicked_product": clicked_product,
        "timestamp": datetime.now().isoformat(),
    }
    ThreadSafeFileWriter.write_log(LOGS_FILE, log_entry)

def has_search_logs():
    """Checks if there's at least one search log."""
    try:
        with open(LOGS_FILE) as log_file:
            logs = [json.loads(line) for line in log_file]
        return any(log["search_query"] for log in logs)
    except FileNotFoundError:
        return False

def check_threshold(threshold=INTERACTION_THRESHOLD):
    """Checks if the user has reached the interaction threshold."""
    try:
        with open(LOGS_FILE) as log_file:
            logs = [json.loads(line) for line in log_file]
        return len(logs) >= threshold
    except FileNotFoundError:
        return False

def recommend_products():
    """Generates recommendations based on user logs."""
    try:
        with open(LOGS_FILE) as log_file:
            logs = [json.loads(line) for line in log_file]
        queries = [log["search_query"] for log in logs]

        # Find top search terms
        popular_terms = Counter(queries).most_common(3)
        recommendations = []
        for term, _ in popular_terms:
            recommendations.extend(search(term)[:3])  # Top 3 results per term

        return recommendations
    except FileNotFoundError:
        return []

# Streamlit Application
def main():
    st.title("Semantic E-Commerce Search with Recommendations")
    
    # Initialize session state
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ''
    if 'search_results' not in st.session_state:
        st.session_state.search_results = []
    if 'viewed_products' not in st.session_state:
        st.session_state.viewed_products = set()
    
    # Search input
    st.session_state.search_query = st.text_input(
        "Search", 
        value=st.session_state.search_query
    )

    # Search button
    if st.button("Search") or st.session_state.search_query:
        with st.spinner("Searching..."):
            if st.session_state.search_query:
                st.session_state.search_results = search(st.session_state.search_query)
                log_interaction(st.session_state.search_query)

        # Display results
        if st.session_state.search_results:
            st.subheader("Search Results")
            for result in st.session_state.search_results:
                if "_source" in result:
                    product = result["_source"]
                    st.header(product["ProductName"])
                    st.text(product["Description"])

                    # Unique key for each product
                    btn_key = f"view_{product['ProductName']}"  # Removed index
                    if st.button(f"View {product['ProductName']}", key=btn_key):
                        if product['ProductName'] not in st.session_state.viewed_products:
                            log_interaction(st.session_state.search_query, product['ProductName'])
                            st.session_state.viewed_products.add(product['ProductName'])
                            st.success(f"Viewed {product['ProductName']}")

    # Recommendations Section
    if has_search_logs() and check_threshold():
        st.markdown("## 🔥 **Recommended Products for You** 🔥")
        recommendations = recommend_products()
        for rec in recommendations:
            if "_source" in rec:
                product = rec["_source"]
                st.header(product["ProductName"])
                st.text(product["Description"])
                st.divider()

if __name__ == "__main__":
    main()
