import { useState } from 'react';
import "../assets/styleLogin.css";


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

        <button type="submit">Iniciar Sesión</button>
        <div id="message">{message}</div>
      </form>
    </div>
  );
};

export default LoginPage;
