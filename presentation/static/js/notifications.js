// Sistema de notificaciones
function showNotification(message, type = 'info', duration = 4000) {
    const container = document.getElementById('notification-container');
    
    // Si no existe el contenedor, crearlo
    if (!container) {
        const newContainer = document.createElement('div');
        newContainer.id = 'notification-container';
        newContainer.className = 'notification-container';
        document.body.appendChild(newContainer);
    }
    
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
    
    const finalContainer = document.getElementById('notification-container');
    finalContainer.appendChild(notification);
    
    // Auto-remove después del tiempo especificado
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => notification.remove(), 300);
        }
    }, duration);
}

// Sistema de confirmación con modal
function showConfirm(options = {}) {
    return new Promise((resolve) => {
        const {
            title = '¿Estás seguro?',
            message = '¿Deseas continuar con esta acción?',
            confirmText = 'Confirmar',
            cancelText = 'Cancelar',
            type = 'danger', // danger, warning, info
            icon = 'fas fa-exclamation-triangle'
        } = options;

        // Crear overlay
        const overlay = document.createElement('div');
        overlay.className = 'confirm-modal-overlay';
        
        // Crear modal
        const modal = document.createElement('div');
        modal.className = 'confirm-modal';
        
        const typeClass = type === 'danger' ? 'danger' : type;
        const headerColor = type === 'danger' ? 'bg-danger' : type === 'warning' ? 'bg-warning' : 'bg-info';
        const iconColor = type === 'danger' ? 'text-danger' : type === 'warning' ? 'text-warning' : 'text-info';
        
        modal.innerHTML = `
            <div class="confirm-modal-header ${headerColor}">
                <div class="confirm-modal-icon-wrapper">
                    <i class="${icon} confirm-modal-icon"></i>
                </div>
            </div>
            <div class="confirm-modal-body">
                <h4 class="confirm-modal-title">${title}</h4>
                <p class="confirm-modal-message">${message}</p>
            </div>
            <div class="confirm-modal-footer">
                <button class="confirm-modal-btn confirm-modal-btn-cancel" data-action="cancel">
                    <i class="fas fa-times me-2"></i>${cancelText}
                </button>
                <button class="confirm-modal-btn confirm-modal-btn-confirm ${typeClass}" data-action="confirm">
                    <i class="fas fa-check me-2"></i>${confirmText}
                </button>
            </div>
        `;
        
        overlay.appendChild(modal);
        document.body.appendChild(overlay);
        
        // Animación de entrada
        setTimeout(() => {
            overlay.classList.add('active');
            modal.classList.add('active');
        }, 10);
        
        // Función para cerrar el modal
        const closeModal = (confirmed) => {
            overlay.classList.remove('active');
            modal.classList.remove('active');
            setTimeout(() => {
                overlay.remove();
                resolve(confirmed);
            }, 300);
        };
        
        // Event listeners
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                closeModal(false);
            }
        });
        
        modal.querySelector('[data-action="cancel"]').addEventListener('click', () => {
            closeModal(false);
        });
        
        modal.querySelector('[data-action="confirm"]').addEventListener('click', () => {
            closeModal(true);
        });
        
        // Cerrar con ESC
        const handleEscape = (e) => {
            if (e.key === 'Escape') {
                closeModal(false);
                document.removeEventListener('keydown', handleEscape);
            }
        };
        document.addEventListener('keydown', handleEscape);
    });
}

// Hacer las funciones disponibles globalmente
window.showNotification = showNotification;
window.showConfirm = showConfirm;
