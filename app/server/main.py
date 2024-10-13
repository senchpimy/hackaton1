from flask import Flask, jsonify, request, session
import MySQLdb
import herramientas

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "plof"
app.config["MYSQL_PASSWORD"] = "pass"
app.config["MYSQL_DB"] = "usuarios_db"

app.secret_key = "pass"

db = MySQLdb.connect(
    app.config["MYSQL_HOST"],
    app.config["MYSQL_USER"],
    app.config["MYSQL_PASSWORD"],
    app.config["MYSQL_DB"],
)


@app.route("/")
def home():
    return "Este es tu servidor de Flask."


@app.route("/login", methods=["GET"])
def login_front():
    str = """
<!DOCTYPE html>
<html>
  <head>
    <title>Enviar JSON</title>
    <script>
      function sendLoginData() {
        const data = {
          username: "miusuario",
          password: "08a417d732e03b18797c81e6f9befd5ef3632f162c5b920e2bec64e89a2dce33"
        };

        fetch('http://localhost:8000/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => console.log('Success:', data))
        .catch(error => console.error('Error:', error));
      }
    </script>
  </head>
  <body>
    <button onclick="sendLoginData()">Enviar JSON</button>
  </body>
</html>
    """
    return str


@app.route("/login", methods=["post"])
def login():
    data = request.get_json()
    user = data["username"]
    passwd = data["password"]

    response = {"status": False}
    cursor = db.cursor()
    try:
        cursor.execute(
            "SELECT contraseña_hash FROM usuarios WHERE nombre_usuario = %s", (user,)
        )
        result = cursor.fetchone()

        if result:
            stored_password_hash = result[0]
            if stored_password_hash == passwd:
                response["status"] = True
            else:
                response["pass"] = stored_password_hash
        else:
            response["message"] = "Usuario no encontrado."

    except Exception as e:
        response["message"] = str(e)
    finally:
        cursor.close()

    return jsonify(response)


@app.route("/acciones", methods=["get"])
def acciones_front():
    stri = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enviar JSON</title>
    <script>
        function enviarJSON() {
            const texto = document.getElementById("inputTexto").value;

            const data = {
                texto: texto
            };
            console.log(data)

            fetch('http://localhost:8000/acciones', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                // Verificamos si la respuesta tiene contenido JSON
                const contentType = response.headers.get("content-type");
                if (contentType && contentType.includes("application/json")) {
                    return response.json();  // Si es JSON, parseamos
                } else {
                    return response.text();  // Si no es JSON, devolvemos el texto
                }
            })
            .then(result => {
                console.log('Respuesta del servidor:', result);
                alert('Datos enviados correctamente: ' + result);
            })
            .catch(error => {
                console.error('Error al enviar:', error);
                alert('Hubo un error al enviar los datos');
            });
        }
    </script>
</head>
<body>
    <h1>Enviar texto como JSON</h1>
    <label for="inputTexto">Ingresa tu texto:</label>
    <textarea id="inputTexto" rows="4" cols="50">Que buen dia no crees?</textarea><br><br>
    <button onclick="enviarJSON()">Enviar</button>
</body>
</html>
    """
    return stri


@app.route("/acciones", methods=["POST"])
def acciones():
    try:
        chat = session["chat"]
        chat.append("")
        chat.pop()
    except:
        chat = []
    llm = herramientas.ChatHackaton()
    data = request.get_json()
    convo = llm.chatear(data["texto"], chat)
    session["chat"] = convo
    resp = {"convo": convo}
    return jsonify(resp)


if __name__ == "__main__":
    # app.run(debug=True, host="0.0.0.0", port=8000)
    app.run(debug=True, port=8000)
