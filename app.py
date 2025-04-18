import os
from functools import lru_cache

import streamlit as st
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI

from prompt import TEMPLATE

load_dotenv()
VECTORSTORE_DIR = "vectorstore"
EMBEDDING_MODEL = OpenAIEmbeddings(api_key=os.environ["OPENAI_API_KEY"])
LLM = ChatOpenAI(temperature=0, api_key=os.environ["OPENAI_API_KEY"])


def format_docs(docs: list[Document]):
    return "\n\n".join(doc.page_content for doc in docs)


@st.cache_resource
@lru_cache
def load_retriever(subject_name: str) -> VectorStoreRetriever:
    persist_dir = os.path.join(VECTORSTORE_DIR, subject_name)
    vectordb = Chroma(persist_directory=persist_dir, embedding_function=EMBEDDING_MODEL)
    return vectordb.as_retriever(search_kwargs={"k": 5})


@st.cache_resource(show_spinner=False)
def generate_answer(subject_name: str, question: str) -> str:
    retriever = load_retriever(subject_name)
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=TEMPLATE.format(subject=subject_name),
    )
    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | LLM
        | StrOutputParser()
    )
    return rag_chain.invoke(question)


st.title("Chat with Your Vectorstore")

store_names: list[str] = [
    name
    for name in os.listdir(VECTORSTORE_DIR)
    if os.path.isdir(os.path.join(VECTORSTORE_DIR, name))
]

if not store_names:
    st.warning("No vector stores found in the 'vectorstore/' directory.")
    st.stop()

subject = st.sidebar.radio("Select a subject:", store_names)

question = st.chat_input("💬 Ask me anything about this subject")

if question:
    with st.chat_message("user"):
        st.markdown(question)

    answer = generate_answer(
        subject_name=subject,
        question=question,
    )

    with st.chat_message("assistant"):
        st.markdown(answer)
