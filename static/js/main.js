// Main JavaScript functionality for AI Image Generator

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize character counter for prompt input
    initializeCharacterCounter();
    
    // Initialize form submission handling
    initializeFormSubmission();
    
    // Initialize image lazy loading
    initializeLazyLoading();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize smooth scrolling
    initializeSmoothScrolling();
});

/**
 * Initialize character counter for prompt textarea
 */
function initializeCharacterCounter() {
    const promptTextarea = document.getElementById('prompt');
    const charCount = document.getElementById('charCount');
    
    if (promptTextarea && charCount) {
        // Update character count on input
        promptTextarea.addEventListener('input', function() {
            const currentLength = this.value.length;
            const maxLength = 500;
            
            charCount.textContent = currentLength;
            
            // Update styling based on character count
            charCount.className = getCharCountClass(currentLength, maxLength);
            
            // Disable submit button if over limit
            const submitButton = document.querySelector('.generate-btn');
            if (submitButton) {
                submitButton.disabled = currentLength > maxLength;
            }
        });
        
        // Auto-resize textarea
        promptTextarea.addEventListener('input', autoResizeTextarea);
    }
}

/**
 * Get appropriate CSS class for character count
 */
function getCharCountClass(current, max) {
    const percentage = (current / max) * 100;
    
    if (percentage >= 100) {
        return 'text-danger fw-bold';
    } else if (percentage >= 90) {
        return 'text-warning fw-semibold';
    } else if (percentage >= 75) {
        return 'text-info';
    } else {
        return 'text-muted';
    }
}

/**
 * Auto-resize textarea based on content
 */
function autoResizeTextarea(event) {
    const textarea = event.target;
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
}

/**
 * Initialize form submission handling
 */
function initializeFormSubmission() {
    const generateForm = document.getElementById('generateForm');
    
    if (generateForm) {
        generateForm.addEventListener('submit', function(e) {
            const submitButton = this.querySelector('.generate-btn');
            const buttonText = submitButton.querySelector('.btn-text');
            const spinner = submitButton.querySelector('.spinner-border');
            
            if (submitButton && buttonText && spinner) {
                // Show loading state
                submitButton.disabled = true;
                buttonText.textContent = 'Generating...';
                spinner.classList.remove('d-none');
                
                // Add visual feedback
                submitButton.classList.add('generating');
            }
        });
    }
}

/**
 * Initialize lazy loading for images
 */
function initializeLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src || img.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[loading="lazy"]').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize smooth scrolling for anchor links
 */
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Show notification message
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    
    notification.innerHTML = `
        <i class="fas fa-${getNotificationIcon(type)} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

/**
 * Get appropriate icon for notification type
 */
function getNotificationIcon(type) {
    const icons = {
        'success': 'check-circle',
        'danger': 'exclamation-triangle',
        'warning': 'exclamation-circle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

/**
 * Utility function to copy text to clipboard
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showNotification('Copied to clipboard!', 'success');
    } catch (err) {
        console.error('Failed to copy: ', err);
        showNotification('Failed to copy to clipboard', 'danger');
    }
}

/**
 * Format file size for display
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Format relative time (e.g., "2 hours ago")
 */
function formatRelativeTime(date) {
    const now = new Date();
    const diffInSeconds = Math.floor((now - date) / 1000);
    
    const intervals = {
        year: 31536000,
        month: 2592000,
        week: 604800,
        day: 86400,
        hour: 3600,
        minute: 60
    };
    
    for (const [unit, seconds] of Object.entries(intervals)) {
        const interval = Math.floor(diffInSeconds / seconds);
        if (interval >= 1) {
            return `${interval} ${unit}${interval !== 1 ? 's' : ''} ago`;
        }
    }
    
    return 'Just now';
}

/**
 * Debounce function to limit rapid function calls
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Check if device is mobile
 */
function isMobile() {
    return window.innerWidth <= 768;
}

/**
 * Add loading state to button
 */
function setButtonLoading(button, loading = true) {
    if (!button) return;
    
    const spinner = button.querySelector('.spinner-border');
    const text = button.querySelector('.btn-text');
    
    if (loading) {
        button.disabled = true;
        if (spinner) spinner.classList.remove('d-none');
        if (text) text.textContent = 'Loading...';
    } else {
        button.disabled = false;
        if (spinner) spinner.classList.add('d-none');
        if (text) text.textContent = button.dataset.originalText || 'Submit';
    }
}

// Global error handler
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    showNotification('An unexpected error occurred. Please refresh the page.', 'danger');
});

// Handle online/offline status
window.addEventListener('online', function() {
    showNotification('Connection restored', 'success');
});

window.addEventListener('offline', function() {
    showNotification('Connection lost. Some features may not work.', 'warning');
});

// Export functions for use in other scripts
window.AIImageGenerator = {
    showNotification,
    copyToClipboard,
    formatFileSize,
    formatRelativeTime,
    debounce,
    isMobile,
    setButtonLoading
};
