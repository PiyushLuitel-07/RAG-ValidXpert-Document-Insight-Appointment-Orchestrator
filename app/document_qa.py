from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS

def setup_document_qa(docs_path: str):
    # Load documents
    if docs_path.startswith('http'):
        loader = WebBaseLoader(docs_path)
    else:
        loader = PyPDFLoader(docs_path)
    documents = loader.load()
    
    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)
    
    # Create vectorstore
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(splits, embeddings)
    retriever = vectorstore.as_retriever()
    
    # Setup LLM
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)
    
    # Create chain
    qa_prompt = ChatPromptTemplate.from_template("""
    Answer the question based only on the following context:
    {context}
    
    Question: {input}
    
    If you don't know the answer, say you don't know. Don't make up an answer.
    """)
    
    document_chain = create_stuff_documents_chain(llm, qa_prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
    return retrieval_chain