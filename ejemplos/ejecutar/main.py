from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage  # Mensaje normal

from langchain_core.tools import tool

messages = [
    (
        "system",
        "You are a helpful assistanistant that sometimes may execute function others you willl talk to the userr",
    ),
]
#
# prompts = []
# with open("./prompts.txt", "r") as f:
#    prompts = f.read().split("\n")
#
# print(prompts)
#
# llm = ChatOllama(
#    model="llama3.1",
#    temperature=0,
#    # other params...
# )
#
# ai_msg = llm.invoke(messages)
#
# print(ai_msg)


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
def ejecutar_funcion(option: bool) -> bool:
    """
    Esta función sirve para saver si el usuario quiere ejecutar una funcion o solo texto, True si el
    usuario quiere ejecutar una funcion o false si solo es texto o informacion
    Las posible funciones que el usuario podria ejecutar son:
        - send_deposit

    Args:
        option (boolean):
    """
    return bool(option)


with open("./prompts.txt", "r") as f:
    cont = f.read()
    coco = cont.split("\n")
    llm = ChatOllama(
        model="llama3.2",
        # model="mistral",
        temperature=0,
        base_url="http://amused-amazed-imp.ngrok-free.app",
    ).bind_tools([ejecutar_funcion])

    # for i in coco:
    while True:
        i = input(">")
        messages.append(("human", i))
        result = llm.invoke(messages)
        print(result)
