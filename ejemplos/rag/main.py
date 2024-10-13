from langchain import hub
from langchain_chroma import Chroma

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)  # Mensaje normal

from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.tools import tool


@tool
def send_deposit(amount: float, recipient: str) -> bool:
    """This function sends a deposit to the specified recipient's account. It requires the amount to send and the recipient's name.

    Args:
        amount (float): The amount of money to deposit.
        recipient (str): The name of the person who will receive the deposit.
    """
    print(f"user_id {amount} addresses {recipient}")
    return True


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


@tool
def create_timer(amount: int, unit: str) -> bool:
    """This function creates a timer for the specified amount of time.
    The unit can either be 'minutes' or 'hours'.

    Args:
        amount (int): The amount of time for the timer.
        unit (str): The unit of time ('minutes' or 'hours').

    Returns:
        bool: Returns True if the timer is successfully set, False otherwise.
    """
    if unit not in ["minutes", "hours"]:
        print("Invalid unit. Please use 'minutes' or 'hours'.")
        return False

    if unit == "hours":
        time_in_minutes = amount * 60
    else:
        time_in_minutes = amount

    print(f"Timer set for {time_in_minutes} minutes.")
    return True


herramientas_lista = [create_timer, send_deposit]
herramientas = {}
for e in herramientas_lista:
    herramientas[e.name] = e

llm_chat = ChatOllama(
    model="llama3.2",
    temperature=0,
    base_url="http://amused-amazed-imp.ngrok-free.app",
)

llm_functions = ChatOllama(
    model="llama3.2",
    temperature=0,
    base_url="http://amused-amazed-imp.ngrok-free.app",
).bind_tools(herramientas_lista)

llm_rag = ChatOllama(
    model="llama3.1",
    temperature=0,
    base_url="http://amused-amazed-imp.ngrok-free.app",
    # ).bind_tools(herramientas_lista)
)

llm_selector = ChatOllama(
    model="llama3.2",
    temperature=0,
    base_url="http://amused-amazed-imp.ngrok-free.app",
).bind_tools([selector])

# ------------------------------RAG-------------------------------------
#
#
#
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


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm_rag
)
# --------------------------------------------------------------------

selector_prompt = PromptTemplate.from_template(
    """
"Based on the following message, determine whether the user wants to chat, request information, or execute one of the following functions:  
- Create a timer  
- Send a deposit  

Message: {text}  
Your response must be one of the following: 'function,' 'chat,' or 'information.'  

The available functions are:  
- Send deposit  
- Create timer."

    """
)

selector_chain = selector_prompt | llm_selector


herramientas_selector = {}
herramientas_selector[selector.name] = selector
mensajes = []
while True:
    i = input(">")
    hu_men = HumanMessage(content=i)
    mensajes.append(hu_men)
    response = selector_chain.invoke(hu_men)
    # -----------Selector de Evento--------------
    t = response.tool_calls
    if t:
        e = t[0]
        print(e["name"])
        try:
            func = herramientas_selector[e["name"]]
            res = func.invoke(e["args"])
            while not res:
                res = func.invoke(e["args"])
            print("--------------------------------")
            print(res)
            response = e["args"]["option"]
            print(response)
            print("--------------------------------")
        except e:
            print(e)
            print("La funcion no existe")
    # -------------------------
    if response == "informacion":
        t = rag_chain.invoke(mensajes)
    elif response == "funcion":
        t = llm_functions.invoke(mensajes)
        print(t)
        continue
    else:
        t = llm_chat.invoke(mensajes)
        print(t)
    mensajes.append(t)
