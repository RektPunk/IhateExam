import glob
import os
from argparse import ArgumentParser

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

load_dotenv()

if __name__ == "__main__":
    parser = ArgumentParser(description="Create vector stores from markdown files.")
    parser.add_argument(
        "--directory", type=str, help="Directory containing markdown files."
    )
    parser.add_argument(
        "--vectorstore-directory", type=str, help="Directory to save vector stores."
    )
    args = parser.parse_args()

    embedding = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    for subject in os.listdir(args.directory):
        subject_path = os.path.join(args.directory, subject)
        if not os.path.isdir(subject_path):
            continue

        md_files = glob.glob(os.path.join(subject_path, "*.md"))
        if not md_files:
            print(f"No .md files found in {subject_path}")
            continue

        all_docs: list[Document] = []
        for file in md_files:
            loader = TextLoader(file, encoding="utf-8")
            documents = loader.load()
            split_docs = text_splitter.split_documents(documents)
            all_docs.extend(split_docs)

        persist_dir = os.path.join(args.vectorstore_directory, subject)
        vectordb = Chroma.from_documents(
            documents=all_docs,
            embedding=embedding,
            persist_directory=persist_dir,
        )
        vectordb.persist()
        print(f"Vector store saved: {subject} → {persist_dir}")
