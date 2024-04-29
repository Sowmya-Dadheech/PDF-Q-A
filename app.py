import streamlit as st
import os
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor

from llama_index.core.response.pprint_utils import pprint_response

from dotenv import load_dotenv
load_dotenv()

os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")

from llama_index.core import VectorStoreIndex,SimpleDirectoryReader,ServiceContext
documents=SimpleDirectoryReader("data").load_data()

def get_response(question):
    index=VectorStoreIndex.from_documents(documents,show_progress=True)
    query_engine=index.as_query_engine()
    retriever=VectorIndexRetriever(index=index,similarity_top_k=4)
    postprocessor=SimilarityPostprocessor(similarity_cutoff=0.60)

    query_engine=RetrieverQueryEngine(retriever=retriever,node_postprocessors=[postprocessor])

    response=query_engine.query(question).response
    print(response)
    return response
    
    # pprint_response(response,show_source=True)
    # answer = print(response)
    # return answer

st.title("Llama Index PDF Query App")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    
if uploaded_file is not None:
    file_path = os.path.join("data", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())
        
    st.success(f"File '{uploaded_file.name}' uploaded successfully.")
    
# Take user input question
input = st.text_input("Enter your question:")

    
if st.button("Get answer"):
    if input:
        # Query the index
        print("button chala")
        response = get_response(input)
        print(response)
            
        # Display response
        st.write("Response:")
        st.write(response)
    else:
        st.write("Please enter a question first.")
