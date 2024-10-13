let users = [];

// Cargar los datos de users.json
async function loadUsers() {
    try {
        const response = await fetch('users.json');
        if (!response.ok) throw new Error('Error al cargar los usuarios');
        users = await response.json();
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('message').textContent = 'Error al cargar los datos de usuarios.';
    }
}

// Evento de envío del formulario
document.getElementById('loginForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();

    // Validación de campos vacíos
    if (!username || !password) {
        document.getElementById('message').textContent = 'Por favor, completa todos los campos.';
        return;
    }

    // Autenticación
    const userExists = users.some(user => user.username === username && user.password === password);
    if (userExists) {
        window.location.href = 'index.html'; // Redirigir a otra página
    } else {
        document.getElementById('message').textContent = 'Credenciales incorrectas.';
    }
});

// Cargar los usuarios al inicializar
loadUsers();
