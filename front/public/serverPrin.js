const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

app.use(express.json()); // Para parsear el JSON

// Ruta para manejar las peticiones
app.post('manejo.js', (req, res) => {
    const peticion = req.body.peticion;

    // Leer el archivo JSON y agregar la nueva petición
    fs.readFile('bdPrin.json', 'utf8', (err, data) => {
        if (err) {
            return res.status(500).send('Error al leer la base de datos');
        }

        const jsonData = JSON.parse(data);
        jsonData.push({ peticion }); // Agregar la nueva petición al array

        // Guardar el nuevo contenido en el archivo
        fs.writeFile('bdPrin.json', JSON.stringify(jsonData, null, 2), (err) => {
            if (err) {
                return res.status(500).send('Error al guardar la base de datos');
            }
            res.json({ message: 'Petición guardada con éxito' });
        });
    });
});

app.listen(PORT, () => {
    console.log(`Servidor escuchando en http://localhost:${3000}`);
});
