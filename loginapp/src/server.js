const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const PORT = 5000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Simulación de autenticación
app.post('/api/login', (req, res) => {
  const { email, password } = req.body;

  // Lógica simple de validación
  if (email === 'test@example.com' && password === 'password123') {
    res.json({ message: 'Login exitoso!' });
  } else {
    res.json({ message: 'Credenciales inválidas' });
  }
});

app.listen(PORT, () => {
  console.log(`Servidor corriendo en http://localhost:${PORT}`);
});
