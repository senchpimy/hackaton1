from langchain_ollama import ChatOllama
from langchain.tools import tool

import rag
import detectar_fraude
import adaptar

personas_cuenta = {
    "adame": 59281,
    "sergio": 59281,
    "juan": 89036,
    "antonio": 11711,
    "felipe": 63445,
}


@tool
def send_deposit(amount: float, recipient: str) -> bool:
    """Esta función envía un depósito a la cuenta especificada del destinatario. Requiere el monto a enviar y el nombre del destinatario.

    Args:
        amount (float): El monto de dinero a depositar.
        recipient (str): El nombre de la persona que recibirá el depósito.
    """
    recipient = recipient.lower()
    cuenta = personas_cuenta.get(recipient)
    if cuenta:
        print("AAAAAAAAAAAAAAAAa")
        if detectar_fraude.check_fraud(cuenta):
            return "La cuenta está registrada como fraude, no se realizó la operación"
    print(f"Cantidad {amount} persona {recipient}")
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
def pay_service(amount: float, service_name: str) -> bool:
    """Esta función realiza el pago de un servicio especificado.

    Args:
        amount (float): El monto del pago.
        service_name (str): El nombre del servicio que se pagará.
    """
    print(f"Pago de {amount} al servicio {service_name}")
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
herramientas = {e.name: e for e in herramientas_lista}


def wrapper(func) -> str:
    res = None
    try:
        res = func()
    except Exception as e:
        print(func.__name__)
        return f"Función ejecutada con error: {str(e)}. Informa al usuario sobre esto."
    if res == True:
        return "Función ejecutada con éxito. Informa al usuario sobre esto."
    return res


class ChatHackaton:
    def __init__(self) -> None:
        self.llm_chat = adaptar.ChatAdaptativo()

        self.llm_functions = ChatOllama(
            model="llama3.2",
            temperature=0,
            base_url="http://amused-amazed-imp.ngrok-free.app",
        ).bind_tools(herramientas_lista)

        self.rag = rag.rag_chain
        self.selector = rag.llm_selector

    def chatear(self, prompt: str, conversacion: list[str]) -> list[str]:
        user_prompt = ("human", prompt)
        conversacion.append(user_prompt)
        # ---------------------------------------
        response = self.selector.invoke(user_prompt)
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
            except Exception as e:
                print(e)
                print("La función no existe")
        # -------------------------
        content = None
        if response == "informacion":
            t = self.rag.invoke(user_prompt[1])
            content = t.content
            print(t)
        elif response == "funcion":
            result = self.llm_functions.invoke(user_prompt[1])
            t = result.tool_calls
            e = t[0]
            func = herramientas.get(e["name"])
            if func:
                print("%%%%%%%%%")
                print(e["name"])
                print("%%%%%%%%%")
                function = lambda: func.invoke(e["args"])

                res = wrapper(function)
                print(t)
                print(res)
                sys_mes = ("system", res)
                conversacion.append(sys_mes)
                content = "Funcion ejecutada"
            else:
                print("La herramienta no existe en 'herramientas'")
        else:
            t = self.llm_chat.chat(user_prompt[1])
            content = t
            print(t)
        if t:
            ai_mes = ("ai", content)
            conversacion.append(ai_mes)

        print(conversacion)
        return conversacion
