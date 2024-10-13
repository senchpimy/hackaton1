document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
  
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
  
    try {
      const response = await fetch('http://localhost:5000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
  
      const data = await response.json();
      if (response.ok) {
        alert('Login successful!');
        localStorage.setItem('token', data.token); // Store token in localStorage
      } else {
        document.getElementById('error').textContent = data.message;
      }
    } catch (error) {
      document.getElementById('error').textContent = 'An error occurred';
    }
  });
  