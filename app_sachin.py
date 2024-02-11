import streamlit as st
# import PyPDF
import string
import os
import base64
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, GPTListIndex
import dotenv
from dotenv import load_dotenv
import openai


load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
openai.api_key = os.getenv("OPENAI_API_KEY")

def semantic_search(query, pdf_path):
    data = SimpleDirectoryReader('data').load_data()
    index = GPTVectorStoreIndex.from_documents(data)
    response = index.query(query)
    return(response)

def summarize(pdf_path):
    data = SimpleDirectoryReader('data').load_data()
    index = GPTListIndex.from_documents(data)
    response = index.query("Summarize the document", response_mode='tree_summarize')
    return response


def save_uploaded_pdf(pdf, pdf_path):
    with open(pdf_path, "wb") as file:
        file.write(pdf.getbuffer())
    return st.success("Saved the {} pdf to directory".format(pdf.name))

def displayPDF(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

st.set_page_config(layout='wide')
st.title("Chat with your documents")

pdf= st.file_uploader("Upload your PDF", type=['pdf'])

# What is the total experience of the candidate?
if pdf is not None:
    col1, col2, col3 = st.columns([2,1,1])

    with col1:
        pdf_path = "data/"+pdf.name
        ip_file = save_uploaded_pdf(pdf, pdf_path)
        display_pdf = displayPDF(pdf_path)

    with col2:
        st.success("Search Area")
        query_search = st.text_area("Search your query")
        if st.checkbox("Search"):
            st.info("Your query"+query_search)
            result = semantic_search(query_search,pdf_path)
            st.write(result)

    with col3:
        st.success("Document summary")
        summary_res = summarize(pdf_path)