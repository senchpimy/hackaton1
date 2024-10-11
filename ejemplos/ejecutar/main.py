from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage  # Mensaje normal

from typing import List

from langchain_core.tools import tool

# messages = [
#    (
#        "system",
#        "You are a helpful assistant that translates English to French. Translate the user sentence.",
#    ),
#    ("human", "I love programming."),
# ]
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


with open("./prompts.txt", "r") as f:
    cont = f.read()
    coco = cont.split("\n")
    llm = ChatOllama(
        model="llama3.2",
        # model="mistral",
        temperature=0,
        base_url="http://amused-amazed-imp.ngrok-free.app",
    ).bind_tools([send_deposit])
    for i in coco:
        result = llm.invoke(
            "Escoge la funcion adecuada y cumple con la siguiente funcion:" f"{i}"
        )
        print(result.tool_calls)
