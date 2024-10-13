const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');

const app = express();
const PORT = 3000;

// Middleware
app.use(bodyParser.json());
app.use(express.static('public'));

// Ruta para manejar el inicio de sesión
app.post('/login', (req, res) => {
    const { username, password } = req.body;

    // Aquí puedes agregar la lógica para validar el usuario
    if (username === 'usuario' && password === 'contraseña') {
        // Generar un archivo JSON con los datos de inicio de sesión
        const userData = { username, timestamp: new Date() };
        fs.writeFileSync('user_data.json', JSON.stringify(userData, null, 2));
        return res.json({ message: 'Inicio de sesión exitoso' });
    }

    res.status(401).json({ message: 'Usuario o contraseña incorrectos' });
});

// Iniciar el servidor
app.listen(PORT, () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);
});
