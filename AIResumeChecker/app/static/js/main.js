// Main JavaScript for Resume Analyzer

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize file upload enhancements
    initializeFileUpload();
    
    // Initialize form validations
    initializeFormValidation();
    
    // Initialize animations
    initializeAnimations();
    
    // Initialize tooltips
    initializeTooltips();
}

function initializeFileUpload() {
    const fileInput = document.getElementById('resume');
    const uploadWrapper = document.querySelector('.file-upload-wrapper');
    const uploadInfo = document.querySelector('.file-upload-info');
    
    if (!fileInput || !uploadWrapper) return;
    
    // Drag and drop functionality
    uploadWrapper.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadWrapper.classList.add('dragover');
        uploadWrapper.style.borderColor = '#3B82F6';
        uploadWrapper.style.backgroundColor = '#EBF4FF';
    });
    
    uploadWrapper.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadWrapper.classList.remove('dragover');
        uploadWrapper.style.borderColor = '#D1D5DB';
        uploadWrapper.style.backgroundColor = '#FAFAFA';
    });
    
    uploadWrapper.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadWrapper.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            updateFileDisplay(files[0]);
        }
    });
    
    // File input change handler
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            updateFileDisplay(file);
        }
    });
    
    function updateFileDisplay(file) {
        const fileName = file.name;
        const fileSize = (file.size / 1024 / 1024).toFixed(2);
        const fileType = file.type;
        
        // Validate file type
        const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword'];
        
        if (!allowedTypes.includes(fileType) && !fileName.toLowerCase().endsWith('.pdf') && !fileName.toLowerCase().endsWith('.docx') && !fileName.toLowerCase().endsWith('.doc')) {
            showAlert('Please upload only PDF or DOCX files.', 'error');
            fileInput.value = '';
            return;
        }
        
        // Validate file size (16MB max)
        if (file.size > 16 * 1024 * 1024) {
            showAlert('File size must be less than 16MB.', 'error');
            fileInput.value = '';
            return;
        }
        
        // Update display
        uploadInfo.innerHTML = `
            <i class="fas fa-file-check fa-2x text-success mb-2"></i>
            <p class="mb-1 fw-semibold text-success">${fileName}</p>
            <small class="text-muted">Size: ${fileSize} MB</small>
        `;
        
        uploadWrapper.style.borderColor = '#10B981';
        uploadWrapper.style.backgroundColor = '#ECFDF5';
    }
}

function initializeFormValidation() {
    const analyzeForm = document.getElementById('analyzeForm');
    
    if (!analyzeForm) return;
    
    analyzeForm.addEventListener('submit', function(e) {
        // Validate form fields
        const jobTitle = document.getElementById('job_title').value.trim();
        const jobDescription = document.getElementById('job_description').value.trim();
        const resumeFile = document.getElementById('resume').files[0];
        
        if (!jobTitle) {
            e.preventDefault();
            showAlert('Please enter a job title.', 'error');
            document.getElementById('job_title').focus();
            return;
        }
        
        if (!jobDescription || jobDescription.length < 50) {
            e.preventDefault();
            showAlert('Please enter a detailed job description (at least 50 characters).', 'error');
            document.getElementById('job_description').focus();
            return;
        }
        
        if (!resumeFile) {
            e.preventDefault();
            showAlert('Please upload your resume.', 'error');
            return;
        }
        
        // Show loading state
        showLoadingModal();
        disableSubmitButton();
    });
}

function showLoadingModal() {
    const loadingModal = document.getElementById('loadingModal');
    if (loadingModal) {
        const modal = new bootstrap.Modal(loadingModal);
        modal.show();
        
        // Add progress simulation
        simulateProgress();
    }
}

function simulateProgress() {
    const progressTexts = [
        'Extracting text from resume...',
        'Analyzing skills and keywords...',
        'Comparing with job requirements...',
        'Calculating match scores...',
        'Generating recommendations...',
        'Finalizing analysis...'
    ];
    
    const loadingText = document.querySelector('#loadingModal .modal-body p');
    if (!loadingText) return;
    
    let currentStep = 0;
    const interval = setInterval(() => {
        if (currentStep < progressTexts.length) {
            loadingText.textContent = progressTexts[currentStep];
            currentStep++;
        } else {
            clearInterval(interval);
        }
    }, 2000);
}

function disableSubmitButton() {
    const submitBtn = document.getElementById('submitBtn');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Analyzing...';
    }
}

function initializeAnimations() {
    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);
    
    // Observe all cards and sections
    document.querySelectorAll('.card, .feature-card').forEach(el => {
        observer.observe(el);
    });
    
    // Animate score cards on results page
    animateScoreCards();
}

function animateScoreCards() {
    const scoreCards = document.querySelectorAll('.metric-value');
    
    scoreCards.forEach(card => {
        const targetValue = parseFloat(card.textContent);
        if (!isNaN(targetValue)) {
            animateNumber(card, 0, targetValue, 1000);
        }
    });
}

function animateNumber(element, start, end, duration) {
    const startTime = Date.now();
    const isPercentage = element.textContent.includes('%');
    
    function update() {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function
        const easeOut = 1 - Math.pow(1 - progress, 3);
        const current = start + (end - start) * easeOut;
        
        element.textContent = current.toFixed(1) + (isPercentage ? '%' : '');
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    update();
}

function initializeTooltips() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function showAlert(message, type = 'info') {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at top of main content
    const main = document.querySelector('main');
    if (main) {
        main.insertBefore(alertDiv, main.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// Utility functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

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

// Export functions for use in other scripts
window.ResumeAnalyzer = {
    showAlert,
    formatFileSize,
    debounce,
    animateNumber
};