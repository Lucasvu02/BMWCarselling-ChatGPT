from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.utils import get_current_folder,get_llm

def get_retrieval(k=3):
    llm = get_llm()
    embeddings = OpenAIEmbeddings()
    faiss_path = get_current_folder()+"/retrieval/faiss_index"
    print(faiss_path)
    vectorstore = FAISS.load_local(faiss_path,embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 3})