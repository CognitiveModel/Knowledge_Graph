import pandas as pd
import numpy as np
import os
from langchain_community.document_loaders import PyPDFLoader, UnstructuredPDFLoader, PyPDFium2Loader
from langchain_community.document_loaders import PyPDFDirectoryLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path
from dotenv import load_dotenv
from helpers.df_helpers import documents2Dataframe
import random
import base64
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")

## This function uses the helpers/prompt function to extract concepts from text
from helpers.df_helpers import df2Graph
from helpers.df_helpers import graph2Df

# Load the environment variables from .env file
load_dotenv()

# from sentence_transformers import SentenceTransformer
# model = SentenceTransformer("all-MiniLM-L6-v2")
## Input data directory
# inputdirectory = Path(f"./data_input/{data_dir}")
## This is where the output csv files will be written

## outputdirectory = Path(f"./data_output/{out_dir}")
# outputdirectory = Path(f"KG/data_output/{out_dir}/")
# outputdirectory = Path("D:/LLM/softwares/dozerdb-5.19.0.0/import")
# load_dotenv()
outputdirectory = os.environ.get("Dozerdb")


def extract_graph():

    # # Dir PDF Loader
    # loader = PyPDFDirectoryLoader(inputdirectory)
    # File Loader
    pdf_file = os.environ.get("PDF_DIR")
    encoded_path = base64.b64encode(pdf_file.encode('utf-8')).decode('utf-8')
    # loader = PyPDFLoader("./data_input/Manash.pdf")
    # print(pdf_file)
    loader = PyPDFLoader(pdf_file)
    # loader = DirectoryLoader(inputdirectory, show_progress=True)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )

    pages = splitter.split_documents(documents)
    print("Number of chunks = ", len(pages))
    print("Page 1 content: \n", pages[0].page_content)
    # pages[1].page_content


    df = documents2Dataframe(pages)
    print(df.shape)
    # df.head()

    ##optional
    # df = df[:5]
    # print(df.shape)

    ## To regenerate the graph with LLM, set this to True
    regenerate = True

    if regenerate:
        concepts_list = df2Graph(df, model='mixtral-8x7b-32768')
        dfg1 = graph2Df(concepts_list)
        # if not os.path.exists(outputdirectory):
        #     os.makedirs(outputdirectory)
        
        # Store embedding of nodes and edges in dataframe

        edge_emb = []
        node1_emb = []
        node2_emb = []

        for i in range(len(dfg1["edge"])):
            edge_emb.append(model.encode(dfg1["edge"][i]))
            node1_emb.append(model.encode(dfg1["node_1"][i]))
            node2_emb.append(model.encode(dfg1["node_2"][i]))
        dfg1['node1_embedding'] = node1_emb
        dfg1['node2_embedding'] = node2_emb
        dfg1['edge_embedding'] = edge_emb

        ## Convert DataFrame to JSON (customize as needed)
        json_string = dfg1.to_json(orient='records')  # 'records' format for a list of dictionaries

        # Specify the directory path
        # if not os.path.exists(outputdirectory):
        #     os.makedirs(outputdirectory)

        # Save JSON to a file
        output_file_path = f"{outputdirectory}/import/{encoded_path}.json"

        with open(output_file_path, 'w') as json_file:
            json_file.write(json_string)
        
        # dfg1.to_csv(outputdirectory/"graph.csv", sep=",", index=False)
        # df.to_csv(outputdirectory/"chunks.csv", sep=",", index=False)
    # else:
    #     dfg1 = pd.read_csv(outputdirectory/"graph.csv", sep=",")

    # dfg1.replace("", np.nan, inplace=True)
    # dfg1.dropna(subset=["node_1", "node_2", 'edge'], inplace=True)
    # dfg1['count'] = 4
    ## Increasing the weight of the relation to 4. 
    ## We will assign the weight of 1 when later the contextual proximity will be calculated.  
    print(dfg1.shape)
    dfg1.head()

