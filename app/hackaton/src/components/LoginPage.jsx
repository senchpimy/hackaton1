import React, { useState } from 'react';
import "../assets/styleLogin.css";

import { invoke } from "@tauri-apps/api/core";

async function enviarAccion(texto) {
  console.log("AAAAAAAAAAAA")
  try {
    const respuesta = await invoke("enviar_accion", { texto });

    if (respuesta) {
      console.log("Respuesta del servidor:", respuesta);
    } else {
      console.log("No se recibió respuesta del servidor.");
    }
  } catch (error) {
    console.error("Error al enviar la acción:", error);
  }

}


// Llamar a la función (por ejemplo, al hacer clic en un botón)

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (username && password) {
      setMessage('Iniciando sesión...');
      // Simular navegación a la página principal
      window.location.href = '/home';
    } else {
      setMessage('Por favor, completa todos los campos.');
    }
  };
  const [texto, setTexto] = useState("Que buen día no crees?");
  const handleClick = () => {
    texto = "Buenos dias"
    enviarAccion(texto); // Llama a la función con el texto del estado
    console.log("AAAAA")
  };

  return (
    <div className="login-container">
      <div className="img">
        <img src="media/logo.png" alt="Logo" />
      </div>
      <h2>Iniciar Sesión</h2>
      <form onSubmit={handleSubmit}>
        <label htmlFor="username">Usuario:</label>
        <input
          type="text"
          id="username"
          name="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        <label htmlFor="password">Contraseña:</label>
        <input
          type="password"
          id="password"
          name="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button onClick={handleClick}>Iniciar Sesión</button>
        <div id="message">{message}</div>
      </form>
    </div>
  );
};

export default LoginPage;
