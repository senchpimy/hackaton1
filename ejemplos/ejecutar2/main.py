from langchain_ollama import ChatOllama
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)  # Mensaje normal

from typing import List

from langchain_core.tools import tool

mensajes = []

system_propmt = "Eres un pirata y siempre vas a intentar mantenerte en personaje"
prompt = SystemMessage(content=system_propmt)
mensajes.append(prompt)


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
llm = ChatOllama(
    model="llama3.1",
    # model="llama3.2",
    temperature=0,
).bind_tools(herramientas_lista)

while True:
    i = input(">")
    hu_mes = HumanMessage(content=i)
    mensajes.append(hu_mes)
    result = llm.invoke(mensajes)

    print("-----------------------")
    t = result.tool_calls
    if t:
        e = t[0]
        print(e["name"])
        print(herramientas.keys())
        try:
            func = herramientas[e["name"]]
            func.invoke(e["args"])
        except e:
            print(e)
            print("La funcion no existe")
    print("%%%%%%%%%%%%%%%%")
    print(result.content)
    print("-----------------------")
    mensajes.append(result)
