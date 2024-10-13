from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain import hub
from langchain_chroma import Chroma

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
    This function analyzes a message to determine whether to execute a function, engage in a conversation, or provide banking-related information based on the message content.

    Response Criteria: The argument must be one of the following options:

        "funcion" (execute a function)
        "conversar" (engage in a conversation)
        "informacion" (provide banking-related information)

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
**Task:** Thoroughly analyze the provided message and accurately determine the user's intention. Classify the intention into one of the following categories:

1. **Engage in a conversation (chat)**
2. **Request information SPECIFICALLY RELATED to BANKING or ECONOMIC TOPICS (informacion)**
3. **Execute one of the following functions:**
   - Send a deposit
   - Recharge a mobile
   - Pay a service
   - Cardless withdrawal

**Message:** {text}

**Instructions for Response:**

- Your response must strictly adhere to one of the following: **'funcion,' 'chat,' or 'informacion.'**
- **Only select 'informacion' if the user is EXPLICITLY REQUESTING INFORMATION THAT IS DIRECTLY RELATED TO BANKING OR ECONOMIC TOPICS.** Any vague or general inquiries must not be classified as 'informacion.'
- Do NOT select 'informacion' for topics unrelated to banking or economics, regardless of context or implication.
- Ensure that your classification is based exclusively on the content of the message provided, without inferring intent beyond the given text.
- Maintain clarity and precision in your classification, avoiding any assumptions or interpretations not supported by the message.
    """
)


herramientas_selector = {}
herramientas_selector[selector.name] = selector

llm_selector = ChatOllama(
    model="llama3.2",
    temperature=0,
    base_url="http://amused-amazed-imp.ngrok-free.app",
).bind_tools([selector])
