document.getElementById('loginForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();
        if (data.success) {
            alert('Inicio de sesión exitoso');
        } else {
            alert('Error en el inicio de sesión');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Ocurrió un error');
    }
});
