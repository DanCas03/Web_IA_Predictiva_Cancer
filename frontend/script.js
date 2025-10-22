/**
 * Script principal para la aplicación de predicción de riesgo de cáncer
 * Maneja la interacción con el formulario y la comunicación con la API
 */

// Configuración de la API
const API_URL = 'http://localhost:5000';

// Referencias a elementos del DOM
const form = document.getElementById('predictionForm');
const resultsSection = document.getElementById('resultsSection');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');

// Event listener para el formulario
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Resetear mensajes de error y resultados
    hideError();
    hideResults();
    
    // Mostrar loader
    showLoader();
    
    try {
        // Recopilar datos del formulario
        const formData = collectFormData();
        
        // Validar datos en el frontend
        const validation = validateFormData(formData);
        if (!validation.isValid) {
            showError(validation.message);
            hideLoader();
            return;
        }
        
        // Enviar datos a la API
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        // Manejar respuesta
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.message || 'Error en la predicción');
        }
        
        // Mostrar resultados
        displayResults(result.prediction);
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'Error al conectar con el servidor. Por favor, intente nuevamente.');
    } finally {
        hideLoader();
    }
});

/**
 * Recopila los datos del formulario
 */
function collectFormData() {
    const data = {};
    
    // Campos numéricos
    const numericFields = ['age', 'bmi', 'liver_function_score', 'alpha_fetoprotein_level'];
    numericFields.forEach(field => {
        const value = document.getElementById(field).value;
        data[field] = parseFloat(value);
    });
    
    // Campos de selección
    const selectFields = ['gender', 'alcohol_consumption', 'smoking_status', 'physical_activity_level'];
    selectFields.forEach(field => {
        data[field] = document.getElementById(field).value;
    });
    
    // Campos checkbox (binarios)
    const checkboxFields = ['hepatitis_b', 'hepatitis_c', 'cirrhosis_history', 'family_history_cancer', 'diabetes'];
    checkboxFields.forEach(field => {
        data[field] = document.getElementById(field).checked ? 1 : 0;
    });
    
    return data;
}

/**
 * Valida los datos del formulario antes de enviar
 */
function validateFormData(data) {
    // Validar campos numéricos
    const numericValidations = {
        age: { min: 0, max: 120, name: 'Edad' },
        bmi: { min: 10, max: 60, name: 'IMC' },
        liver_function_score: { min: 0, max: 100, name: 'Puntuación de función hepática' },
        alpha_fetoprotein_level: { min: 0, max: 1000, name: 'Nivel de alfa-fetoproteína' }
    };
    
    for (const [field, validation] of Object.entries(numericValidations)) {
        const value = data[field];
        
        if (isNaN(value)) {
            return {
                isValid: false,
                message: `${validation.name} debe ser un número válido`
            };
        }
        
        if (value < validation.min || value > validation.max) {
            return {
                isValid: false,
                message: `${validation.name} debe estar entre ${validation.min} y ${validation.max}`
            };
        }
    }
    
    // Validar campos de selección
    const selectFields = ['gender', 'alcohol_consumption', 'smoking_status', 'physical_activity_level'];
    for (const field of selectFields) {
        if (!data[field]) {
            return {
                isValid: false,
                message: `Por favor, seleccione una opción para ${getFieldLabel(field)}`
            };
        }
    }
    
    return { isValid: true };
}

/**
 * Muestra los resultados de la predicción
 */
function displayResults(prediction) {
    // Actualizar porcentaje
    const percentageElement = document.getElementById('riskPercentage');
    const riskLabelElement = document.getElementById('riskLabel');
    const actionMessageElement = document.getElementById('actionMessage');
    const messageIconElement = document.getElementById('messageIcon');
    const messageTextElement = document.getElementById('messageText');
    const gaugeFillElement = document.getElementById('gaugeFill');
    
    // Establecer valores
    percentageElement.textContent = prediction.risk_percentage.toFixed(1);
    
    // Determinar clase de riesgo
    const isHighRisk = prediction.risk_percentage > 50;
    const riskClass = isHighRisk ? 'risk-high' : 'risk-low';
    
    // Actualizar etiqueta de riesgo
    riskLabelElement.textContent = isHighRisk ? 'RIESGO ALTO' : 'RIESGO BAJO';
    riskLabelElement.className = `risk-label ${riskClass}`;
    percentageElement.className = `percentage-value ${riskClass}`;
    
    // Actualizar mensaje de acción
    messageIconElement.textContent = isHighRisk ? '🚨' : '✅';
    messageTextElement.textContent = prediction.risk_message;
    actionMessageElement.className = `action-message ${riskClass}`;
    
    // Actualizar gauge
    gaugeFillElement.style.width = `${prediction.risk_percentage}%`;
    
    // Animar la aparición con un pequeño retraso
    setTimeout(() => {
        // Animar el porcentaje
        animateValue(percentageElement, 0, prediction.risk_percentage, 1000);
        
        // Animar el gauge
        gaugeFillElement.style.width = `${prediction.risk_percentage}%`;
    }, 100);
    
    // Mostrar sección de resultados
    resultsSection.style.display = 'block';
    
    // Scroll suave a los resultados
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

/**
 * Anima un valor numérico
 */
function animateValue(element, start, end, duration) {
    const range = end - start;
    const startTime = Date.now();
    
    const animate = () => {
        const now = Date.now();
        const progress = Math.min((now - startTime) / duration, 1);
        const value = start + (range * easeOutQuad(progress));
        
        element.textContent = value.toFixed(1);
        
        if (progress < 1) {
            requestAnimationFrame(animate);
        }
    };
    
    animate();
}

/**
 * Función de easing para animaciones
 */
function easeOutQuad(t) {
    return t * (2 - t);
}

/**
 * Muestra el loader en el botón
 */
function showLoader() {
    const btnText = document.querySelector('.btn-text');
    const btnLoader = document.querySelector('.btn-loader');
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline';
    form.querySelector('button[type="submit"]').disabled = true;
}

/**
 * Oculta el loader en el botón
 */
function hideLoader() {
    const btnText = document.querySelector('.btn-text');
    const btnLoader = document.querySelector('.btn-loader');
    btnText.style.display = 'inline';
    btnLoader.style.display = 'none';
    form.querySelector('button[type="submit"]').disabled = false;
}

/**
 * Muestra un mensaje de error
 */
function showError(message) {
    errorText.textContent = message;
    errorMessage.style.display = 'block';
    errorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

/**
 * Oculta el mensaje de error
 */
function hideError() {
    errorMessage.style.display = 'none';
}

/**
 * Oculta la sección de resultados
 */
function hideResults() {
    resultsSection.style.display = 'none';
}

/**
 * Resetea el formulario y oculta resultados
 */
function resetForm() {
    form.reset();
    hideResults();
    hideError();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Obtiene la etiqueta legible de un campo
 */
function getFieldLabel(fieldName) {
    const labels = {
        gender: 'Género',
        alcohol_consumption: 'Consumo de alcohol',
        smoking_status: 'Estado de fumador',
        physical_activity_level: 'Nivel de actividad física'
    };
    return labels[fieldName] || fieldName;
}

// Validación en tiempo real para campos numéricos
document.querySelectorAll('input[type="number"]').forEach(input => {
    input.addEventListener('input', function() {
        const min = parseFloat(this.min);
        const max = parseFloat(this.max);
        const value = parseFloat(this.value);
        
        if (value < min) {
            this.value = min;
        } else if (value > max) {
            this.value = max;
        }
    });
});

// Verificar conexión con la API al cargar la página
window.addEventListener('load', async () => {
    try {
        const response = await fetch(`${API_URL}/health`);
        const health = await response.json();
        
        if (health.status !== 'healthy') {
            showError('⚠️ El servidor de predicción no está disponible. Por favor, contacte al administrador.');
        }
    } catch (error) {
        console.error('Error verificando la salud del servidor:', error);
        showError('⚠️ No se puede conectar con el servidor. Asegúrese de que la API esté en ejecución.');
    }
});

// Manejar tecla Enter en campos de formulario
form.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && e.target.tagName !== 'BUTTON') {
        e.preventDefault();
        const formElements = Array.from(form.elements);
        const currentIndex = formElements.indexOf(e.target);
        const nextElement = formElements[currentIndex + 1];
        
        if (nextElement && nextElement.tagName !== 'BUTTON') {
            nextElement.focus();
        }
    }
});
