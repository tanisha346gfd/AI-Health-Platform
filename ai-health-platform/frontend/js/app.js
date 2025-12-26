const API_URL = 'http://localhost:8000/api/v1';


function showTab(tab) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelector(`[onclick="showTab('${tab}')"]`).classList.add('active');
    document.getElementById('registerForm').style.display = tab === 'register' ? 'flex' : 'none';
}



document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                email: formData.get('email'),
                password: formData.get('password'),
                full_name: formData.get('fullName'),
                age: parseInt(formData.get('age')) || null
            })
        });
        if (response.ok) {
            alert('Registration successful!');
            window.location.href = 'dashboard.html';
        } else {
            alert('Registration failed');
        }
    } catch (err) {
        alert('Error: ' + err.message);
    }
});