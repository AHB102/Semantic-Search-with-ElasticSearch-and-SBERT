import pandas as pd
from models.embeddings import EmbeddingModel

model = EmbeddingModel()

def prepare_data(filepath):
    df = pd.read_csv(filepath).loc[:499]
    df.fillna("None", inplace=True)

    df['DescriptionVector'] = df['Description'].apply(lambda x : model.encode_text(x))
    df['ProductNameVecor'] = df['ProductName'].apply(lambda x : model.encode_text(x))
    return df

