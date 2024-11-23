from elasticsearch import Elasticsearch
from data_preparation import prepare_data
# from index_to_pinecone import 

#Prepare the data
filename = "data\myntra_products_catalog.csv"
dataframe = prepare_data(filename)
