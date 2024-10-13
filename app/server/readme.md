# Asistente de IA: Servidor Flask

Este proyecto es la mitad de un servidor de asistente de inteligencia artificial construido con Flask. La aplicación está diseñada para ejecutar ciertas funciones, utilizar RAG (Recuperación Aumentada de Generación), y mantener conversaciones con los usuarios, adaptando su estilo de comunicación según el contexto.

## Tabla de Contenidos

- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Rutas de la API](#rutas-de-la-api)
- [Funciones de Herramientas](#funciones-de-herramientas)
- [Capacidades del Asistente de IA](#capacidades-del-asistente-de-ia)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

## Requisitos

- Python 
- Flask
- MySQLdb
- LangChain

## Instalación
### Ejecución con Docker y Docker Compose

1. Asegúrate de tener [Docker](https://www.docker.com/get-started) y [Docker Compose](https://docs.docker.com/compose/) instalados en tu máquina.

```bash
docker-compose up --build

```

La aplicación estará disponible en http://localhost:8000


## Configuración

1. Configura los detalles de la conexión a la base de datos en el archivo de la aplicación. Ajusta los siguientes parámetros según sea necesario:

   ```python
   app.config["MYSQL_HOST"] = "mysql"  # Cambia a "localhost" si es necesario
   app.config["MYSQL_USER"] = "plof"
   app.config["MYSQL_PASSWORD"] = "pass"
   app.config["MYSQL_DB"] = "usuarios_db"
   ```

2. Asegúrate de que existe una base de datos llamada `usuarios_db` y una tabla `usuarios` con una columna `nombre_usuario` y `contraseña_hash`.

## Uso

Para iniciar la aplicación, ejecuta el siguiente comando:

```bash
python <nombre del archivo>.py
```

La aplicación estará disponible en `http://localhost:8000`.

## Rutas de la API

- **GET /**  
  Devuelve un mensaje simple indicando que el servidor está en funcionamiento.

- **GET /login**  
  Proporciona una interfaz web para enviar datos de inicio de sesión.

- **POST /login**  
  Recibe un JSON con el nombre de usuario y la contraseña. Devuelve un JSON que indica si el inicio de sesión fue exitoso.

  **Ejemplo de JSON de entrada:**
  ```json
  {
      "username": "miusuario",
      "password": "08a417d732e03b18797c81e6f9befd5ef3632f162c5b920e2bec64e89a2dce33"
  }
  ```

- **GET /acciones**  
  Proporciona una interfaz web para enviar texto como JSON.

- **POST /acciones**  
  Recibe un JSON con texto y devuelve una respuesta procesada.

  **Ejemplo de JSON de entrada:**
  ```json
  {
      "texto": "Que buen dia no crees?"
  }
  ```

## Funciones de Herramientas

La aplicación incluye varias herramientas para realizar operaciones bancarias y otras funcionalidades. Estas funciones se integran utilizando la biblioteca LangChain y son invocadas a través de una interfaz de chat.

### Herramientas Disponibles

1. **send_deposit(amount: float, recipient: str) -> bool**  
   Envía un depósito a la cuenta especificada del destinatario.

2. **recharge_mobile(amount: float, phone_number: str) -> bool**  
   Realiza una recarga a un número de teléfono especificado.

3. **pay_service(amount: float, service_name: str) -> bool**  
   Realiza el pago de un servicio especificado.

4. **cardless_withdrawal(amount: float, withdrawal_code: str) -> bool**  
   Realiza un retiro sin tarjeta utilizando un código de retiro.

### Ejemplo de Uso de Herramientas

Los usuarios pueden solicitar operaciones a través de texto, que luego son procesadas y ejecutadas por las herramientas correspondientes, todo mientras se mantiene una conversación fluida.

## Capacidades del Asistente de IA

El asistente de IA tiene varias capacidades avanzadas que le permiten interactuar de manera efectiva con los usuarios y proporcionar respuestas relevantes y personalizadas.

### Obtención de Información mediante RAG

El asistente utiliza un enfoque de Recuperación Aumentada de Generación (RAG) para obtener información relevante y precisa. Este enfoque combina la búsqueda de información con la generación de texto, permitiendo al asistente realizar las siguientes acciones:

1. **Búsqueda de Información:** Cuando un usuario hace una pregunta o solicita información, el asistente utiliza un sistema de búsqueda para recuperar datos relevantes de una base de datos o de fuentes externas. Esto le permite acceder a una amplia gama de conocimientos y responder a consultas específicas.

2. **Generación de Respuestas:** Una vez que se ha recuperado la información pertinente, el asistente genera una respuesta coherente y comprensible. Esta respuesta se elabora utilizando modelos de lenguaje que pueden sintetizar y presentar la información de manera clara.

3. **Adaptación Continua:** El sistema RAG no solo se basa en datos estáticos, sino que también puede aprender y adaptarse con el tiempo. A medida que los usuarios interactúan con el asistente, este puede mejorar sus respuestas y ajustar su enfoque según el contexto y las preferencias del usuario.

### Adaptación a la Forma de Escribir de Cada Usuario

El asistente es capaz de adaptarse al estilo de escritura de cada usuario mediante las siguientes características:

1. **Análisis del Lenguaje Natural:** A lo largo de las interacciones, el asistente analiza el lenguaje utilizado por el usuario, identificando patrones y características específicas de su estilo de comunicación. Esto incluye aspectos como el tono, el vocabulario y la estructura de las oraciones.

2. **Personalización de Respuestas:** Con base en el análisis anterior, el asistente ajusta sus respuestas para que coincidan con la forma de escribir del usuario. Por ejemplo, si un usuario tiende a usar un lenguaje más formal o técnico, el asistente adoptará un estilo similar en sus respuestas. Por otro lado, si el usuario utiliza un lenguaje coloquial y amigable, el asistente responderá de manera más casual.

3. **Contexto Conversacional:** El asistente mantiene un registro de las conversaciones anteriores y el contexto en el que se desarrollan. Esto le permite recordar detalles importantes sobre las preferencias y el estilo de escritura del usuario, lo que resulta en una experiencia más fluida y personalizada.

En resumen, el asistente de IA no solo responde preguntas y realiza funciones, sino que también se adapta continuamente a las necesidades y preferencias de los usuarios, mejorando así la calidad de la interacción.

Este texto proporciona una explicación clara sobre cómo el asistente utiliza RAG para obtener información y cómo se adapta al estilo de escritura de los usuarios. Si necesitas más ajustes o adiciones, ¡házmelo saber!
