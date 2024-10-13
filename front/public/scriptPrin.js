    document.getElementById('enviarBtn').addEventListener('click', function() {
        const peticion = document.getElementById('peticionInput').value;

        // Verificar que el input no esté vacío
        if (peticion.trim() === "") {
            alert("Por favor, escribe una petición.");
            return;
        }

        // Enviar la petición a tu archivo JS que maneja la base de datos
        fetch('manejo.js', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ peticion: peticion })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la petición');
            }
            return response.json();
        })
        .then(data => {
            console.log('Respuesta del servidor:', data);
            // Aquí puedes hacer algo con la respuesta si es necesario
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

