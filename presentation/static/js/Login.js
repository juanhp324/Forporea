document.addEventListener('DOMContentLoaded', function(){
    
    init();
    
    function init() {
        hideLoading();
        setupEventListeners();
    }
    
    function setupEventListeners() {
        const loginForm = document.getElementById('loginForm');
        const togglePassword = document.getElementById('togglePassword');
        
        if (loginForm) {
            loginForm.addEventListener('submit', handleLogin);
        }
        
        if (togglePassword) {
            togglePassword.addEventListener('click', togglePasswordVisibility);
        }
        
        const inputs = document.querySelectorAll('.form-control');
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.style.transform = 'scale(1.02)';
                this.parentElement.style.transition = 'all 0.3s ease';
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.style.transform = 'scale(1)';
            });
        });
    }
    
    function showLoading() {
        document.getElementById('loadingOverlay').style.display = 'flex';
    }
    
    function hideLoading() {
        document.getElementById('loadingOverlay').style.display = 'none';
    }

    function showNotification(message, type = 'info', duration = 4000) {
        const container = document.getElementById('notification-container');
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        
        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        };
        
        notification.innerHTML = `
            <div class="notification-content">
                <i class="${icons[type]} notification-icon"></i>
                <span class="notification-message">${message}</span>
                <button class="notification-close" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        container.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, duration);
    }
    
    function togglePasswordVisibility() {
        const passwordInput = document.getElementById('inputPassword');
        const toggleIcon = document.querySelector('#togglePassword i');
        
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            toggleIcon.className = 'fas fa-eye-slash';
        } else {
            passwordInput.type = 'password';
            toggleIcon.className = 'fas fa-eye';
        }
    }
    
    async function handleLogin(event) {
        event.preventDefault();
        
        const email = document.getElementById('inputEmail').value.trim();
        const password = document.getElementById('inputPassword').value;
        
        if (!email || !password) {
            showNotification('Por favor, completa todos los campos', 'warning');
            return;
        }
        
        if (!isValidEmail(email)) {
            showNotification('Por favor, ingresa un email válido', 'warning');
            return;
        }
        
        const loginData = {
            email: email,
            password: password
        };
        
        showLoading();
        
        try {
            const response = await fetch('/Login', { 
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(loginData)
            });
            
            const result = await response.json();
            
            if (response.ok && result.success) {
                showNotification('¡Inicio de sesión exitoso! Redirigiendo...', 'success', 2000);
                
                setTimeout(() => {
                    if (result.redirect) {
                        window.location.href = result.redirect;
                    } else {
                        window.location.href = '/inicio';
                    }
                }, 1500);
                
            } else {
                const errorMessage = result.message || 'Credenciales incorrectas';
                showNotification(errorMessage, 'error');
                
                document.getElementById('inputPassword').value = '';
                document.getElementById('inputEmail').focus();
            }
            
        } catch (error) {
            console.error('Error de conexión:', error);
            showNotification('Error de conexión. Por favor, inténtalo de nuevo.', 'error');
        } finally {
            hideLoading();
        }
    }
    
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    setTimeout(() => {
        showNotification('¡Bienvenido a Forporea! Inicia sesión para continuar.', 'info', 3000);
    }, 1000);
});
