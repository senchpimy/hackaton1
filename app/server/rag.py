from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain import hub
from langchain_chroma import Chroma

from langchain_core.messages import (
    HumanMessage,
)  # Mensaje normal

from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.tools import tool

modelPath = "sentence-transformers/all-MiniLM-l6-v2"

model_kwargs = {"device": "cpu"}

encode_kwargs = {"normalize_embeddings": False}
loader = PyPDFLoader(file_path="./archivo.pdf")
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
embeddings = HuggingFaceEmbeddings(
    model_name=modelPath,  # Provide the pre-trained model's path
    model_kwargs=model_kwargs,  # Pass the model configuration options
    encode_kwargs=encode_kwargs,  # Pass the encoding options
)
vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)

retriever = vectorstore.as_retriever()
prompt = hub.pull("rlm/rag-prompt")


llm_rag = ChatOllama(
    model="llama3.1",
    temperature=0,
    base_url="http://amused-amazed-imp.ngrok-free.app",
    # ).bind_tools(herramientas_lista)
)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm_rag
)

# -------------------_Selecotor--------------------


@tool
def selector(option: str) -> bool:
    """
    This function analyzes a message and determines whether to execute a function, engage in a conversation, or provide information based on the content of the message.
    The argument must only be one of the following:
        - "funcion" (execute a function)
        - "conversar" (chat)
        - "informacion" (provide information)

    The available functions are:
        - send deposit
        - create timer

    Args:
        option (str): A string specifying the type of request.

    Returns:
        bool: Returns True if the provided option is valid (i.e., 'funcion', 'conversar', or 'informacion'). Returns False if the option is invalid.
    """
    funciones_keywords = ["funcion", "conversar", "informacion"]
    if option not in funciones_keywords:
        return False

    return True


selector_prompt = PromptTemplate.from_template(
    """
"Based on the following message, determine whether the user wants to:  
1. Engage in conversation (chat)  
2. Request information about a bank or economic topics (information)  
3. Execute one of the following functions:  
   - Send a deposit  
   - Recharge a mobile
   - Pay a service
   - Cardless withdraw

Message: {text}  

Your response must be one of the following: 'funcion,' 'chat,' or 'informacion.'  

Only choose 'informacion' if the user is requesting data related to banks or economics."
    """
)


herramientas_selector = {}
herramientas_selector[selector.name] = selector

llm_selector = ChatOllama(
    model="llama3.2",
    temperature=0,
    base_url="http://amused-amazed-imp.ngrok-free.app",
).bind_tools([selector])
