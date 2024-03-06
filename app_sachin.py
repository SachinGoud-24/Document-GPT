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
st.set_page_config(layout="wide")
st.title("Chat with your documents")

st.write("key = ", openai.api_key)


def semantic_search(query):
    data = SimpleDirectoryReader("data").load_data()
    index = GPTVectorStoreIndex.from_documents(data, show_progress=True)
    query_engine = index.as_query_engine()
    response = query_engine.query(query)

    return response


def summarize():
    data = SimpleDirectoryReader("data").load_data()
    index = GPTListIndex.from_documents(data)
    query_engine = index.as_query_engine(
        response_mode="tree_summarize", verbose=True, streaming=True
    )
    response = query_engine.query("Summarize the document")
    return response


def save_uploaded_pdf(pdf, pdf_path):
    with open(pdf_path, "wb") as file:
        file.write(pdf.getbuffer())
    return st.success("Saved the {} pdf to directory".format(pdf.name))


def displayPDF(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")

    # Embedding PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)


pdf = st.file_uploader("Upload your PDF", type=["pdf"])


if pdf is not None:
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        pdf_path = "data/" + pdf.name
        ip_file = save_uploaded_pdf(pdf, pdf_path)
        display_pdf = displayPDF(pdf_path)

    with col2:
        st.success("Search Area")
        query_search = st.text_area("Search your query")
        if st.button("Search"):
            st.info("Your query: " + query_search)

            result = semantic_search(query_search)
            st.text_area("Output", value=result, height=300)

    with col3:
        st.success("Document summary")
        if st.button("Generate Summary"):
            st.info("Generating the document summary...")
            summary_res = summarize()
            st.text_area("Output", value=summary_res, height=500)
