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
import rag


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
def recharge_mobile(amount: float, phone_number: str) -> bool:
    """Esta función realiza una recarga a un número de teléfono especificado.

    Args:
        amount (float): El monto de dinero a recargar.
        phone_number (str): El número de teléfono que recibirá la recarga.
    """
    print(f"Recarga de {amount} al número {phone_number}")
    return True


@tool
def pay_service(amount: float, service_name: str, account_number: str) -> bool:
    """Esta función realiza el pago de un servicio especificado.

    Args:
        amount (float): El monto del pago.
        service_name (str): El nombre del servicio que se pagará.
        account_number (str): El número de cuenta asociado al servicio.
    """
    print(f"Pago de {amount} al servicio {service_name} con cuenta {account_number}")
    return True


@tool
def cardless_withdrawal(amount: float, withdrawal_code: str) -> bool:
    """Esta función realiza un retiro sin tarjeta utilizando un código de retiro.

    Args:
        amount (float): El monto a retirar.
        withdrawal_code (str): El código que permite realizar el retiro sin tarjeta.
    """
    print(f"Retiro sin tarjeta de {amount} usando el código {withdrawal_code}")
    return True


herramientas_lista = [send_deposit, recharge_mobile, pay_service, cardless_withdrawal]
herramientas = {}
for e in herramientas_lista:
    herramientas[e.name] = e


def wrapper(func) -> str:
    try:
        func()
        return "Funcion ejecutada con exito informa al usuario sobre esto"
    except Exception as e:
        return f"Funcion ejecutada con error {str(e)} informa al usuario sobre esto"


class ChatHackaton:
    def __init__(self) -> None:
        self.llm_chat = ChatOllama(
            model="llama3.2",
            temperature=0,
            base_url="http://amused-amazed-imp.ngrok-free.app",
        )

        self.llm_functions = ChatOllama(
            model="llama3.2",
            temperature=0,
            base_url="http://amused-amazed-imp.ngrok-free.app",
        ).bind_tools(herramientas_lista)

        self.rag = rag.rag_chain
        self.selector = rag.llm_selector

    def chatear(self, prompt: str, conversacion: list[str]) -> list[str]:
        user_propmt = ("human", prompt)
        conversacion.append(user_propmt)
        # ---------------------------------------
        response = self.selector.invoke(user_propmt)
        t = response.tool_calls
        if t:
            e = t[0]
            print(e["name"])
            try:
                func = rag.herramientas_selector[e["name"]]
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
        content = None
        if response == "informacion":
            t = self.rag.invoke(user_propmt[1])
            content = t.content
            print(t)
        elif response == "funcion":
            result = self.llm_functions.invoke(user_propmt[1])
            t = result.tool_calls
            e = t[0]
            func = herramientas[e["name"]]
            print("%%%%%%%%%")
            print(e["name"])
            print("%%%%%%%%%")

            def fun():
                func.invoke(e["args"])

            res = wrapper(fun)
            print(t)
            print(res)
            sys_mes = ("system", res)
        else:
            t = self.llm_chat.invoke(conversacion)
            content = t.content
            print(t)
        if t:
            ai_mes = ("ai", content)
            conversacion.append(ai_mes)

        #    res = wrapper(fun)
        #    sys_mes = ("ai", res)
        #    conversacion.append(sys_mes)
        #    content = self.chat.invoke(conversacion)
        #    while content.content == "":
        #        content = self.chat.invoke(conversacion)
        #    content = content.content
        # else:
        #    content = result.content
        # ---------------------------------------
        print(conversacion)
        return conversacion
