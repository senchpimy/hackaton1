from langchain_core.prompts.base import BasePromptTemplate
from langchain_ollama import ChatOllama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate

llm = ChatOllama(
    model="llama3.2", temperature=0, base_url="http://amused-amazed-imp.ngrok-free.app"
)


def analizar_estilo_usuario(texto_usuario):
    prompt_analisis = HumanMessage(
        content=f"Describe el estilo de comunicación del siguiente texto de un usuario: '{texto_usuario}'. Informa sobre el tono, formalidad, uso de lenguaje y cualquier otro aspecto relevante de su forma de hablar pero se breve."
    )

    descripcion_estilo = llm.invoke([prompt_analisis])

    return descripcion_estilo.content


def ajustar_respuesta(respuesta_modelo, descripcion_estilo):
    prompt_adaptado = HumanMessage(
        content=f"Responde de acuerdo con el siguiente estilo de usuario: '{descripcion_estilo}'. Aquí está la respuesta original: '{respuesta_modelo}'."
    )

    respuesta_adaptada = llm.invoke([prompt_adaptado])

    return respuesta_adaptada.content


memory = ConversationBufferMemory()


class ChatAdaptativo:
    def __init__(self) -> None:
        selector_prompt = PromptTemplate(
            input_variables=["history", "input"],
            template="Conversación actual: {history}\n\nUsuario: {input}\nIA: ",
        )
        self.conversation = ConversationChain(
            llm=llm, memory=memory, verbose=True, prompt=selector_prompt
        )
        self.descripcion_estilo_anterior = ""

    def interactuar_con_usuario(self, texto_usuario):
        descripcion_estilo_actual = analizar_estilo_usuario(texto_usuario)

        respuesta_modelo = self.conversation.predict(input=texto_usuario)

        if self.descripcion_estilo_anterior:
            respuesta_final = ajustar_respuesta(
                respuesta_modelo, self.descripcion_estilo_anterior
            )
        else:
            respuesta_final = respuesta_modelo  # Si es la primera vez, no adaptamos

        self.descripcion_estilo_anterior = descripcion_estilo_actual

        return respuesta_final, descripcion_estilo_actual

    def chat(self, propmt: str):
        self.respuesta, self.estilo = self.interactuar_con_usuario(propmt)
        print(f"IA: {self.respuesta}")
        print(f"Descripción del estilo: {self.estilo}\n")  # Separar con una nueva línea
        print("AAAAAAAAAAAAAAAAAAAAAAAaaa")
        print(self.estilo)
        print("AAAAAAAAAAAAAAAAAAAAAAAaaa")
        return self.respuesta
