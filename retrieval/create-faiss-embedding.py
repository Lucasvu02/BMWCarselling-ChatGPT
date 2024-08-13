from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.utils import get_llm
llm = get_llm()
def create_vectorstore(path):
    loader = DirectoryLoader(path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024,chunk_overlap=100)
    documents = text_splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings()
    vectorstore= FAISS.from_documents(documents,embeddings)
    vectorstore.save_local("faiss_index")
    vectorstore = FAISS.load_local("faiss_index",embeddings)
    return vectorstore
vectorstore = create_vectorstore("../data/")
retrieval= vectorstore.as_retriever()





'''
llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.2)
prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ('user','{input}'),
    ('user','Given the above conversation, generate a search query to look up in order to get relevant to the conversation')
]
)
retrieval_chain = create_history_aware_retriever(llm,retrieval,prompt)
chat_history = [
    HumanMessage(content="Is there anything new about Langchain 0.1.0"),
    AIMessage(content="YES")
]
output = retrieval_chain.invoke({
    "chat_history":chat_history,
    'input':"What is news about langchain v0.1.0"
})
print(output[0])

'''
#create c


