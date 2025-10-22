# 🎨 Guía del Frontend - Sistema de Predicción de Cáncer

## Descripción General

El frontend es una **WebApp moderna, intuitiva y completamente responsive** que proporciona una interfaz profesional para la predicción de riesgo de cáncer de hígado.

## ✨ Características Principales

### 1. **Diseño Intuitivo**
- Interfaz limpia y profesional con diseño médico
- Navegación clara y flujo de usuario optimizado
- Formulario organizado por secciones lógicas
- Validación en tiempo real con feedback visual

### 2. **Responsive Design**
- Adaptación perfecta a todos los dispositivos:
  - 📱 **Móviles** (< 480px)
  - 📱 **Tablets** (480px - 768px)
  - 💻 **Desktop** (768px - 1024px)
  - 🖥️ **Large Screens** (> 1024px)
- Grid layout adaptativo
- Elementos que se reorganizan automáticamente

### 3. **Comunicación con Backend (Fetch API)**

#### Ejemplo de Uso Completo:

```javascript
// Configuración de la API
const API_URL = 'http://localhost:5000';

// Datos del paciente a enviar
const patientData = {
    age: 55,
    gender: "Male",
    bmi: 28.5,
    alcohol_consumption: "Regular",
    smoking_status: "Former",
    physical_activity_level: "Moderate",
    liver_function_score: 65.5,
    alpha_fetoprotein_level: 15.3,
    hepatitis_b: 0,
    hepatitis_c: 0,
    cirrhosis_history: 1,
    family_history_cancer: 1,
    diabetes: 0
};

// Realizar predicción
async function getPrediction() {
    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(patientData)
        });
        
        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }
        
        const result = await response.json();
        console.log('Predicción:', result);
        
        // Resultado esperado:
        // {
        //   success: true,
        //   prediction: {
        //     risk_percentage: 67.5,
        //     risk_probability: 0.675,
        //     risk_level: "alto",
        //     risk_message: "Alerta: Cita clínica inmediata.",
        //     action_required: "immediate"
        //   },
        //   timestamp: "2024-01-15T10:30:00"
        // }
        
    } catch (error) {
        console.error('Error:', error);
    }
}
```

#### Health Check:

```javascript
// Verificar estado del servidor
async function checkHealth() {
    const response = await fetch(`${API_URL}/health`);
    const health = await response.json();
    
    if (health.status === 'healthy') {
        console.log('✅ API disponible');
    } else {
        console.error('❌ API no disponible');
    }
}
```

### 4. **Visualización de Resultados**

#### Elementos Visuales Destacados:

1. **Círculo SVG Animado**
   - Indicador circular de progreso
   - Animación fluida del 0 al porcentaje final
   - Cambio de color según riesgo (verde/rojo)

2. **Gauge de Riesgo**
   - Barra horizontal con gradiente
   - Marcador animado que indica el nivel exacto
   - Etiquetas claras de rangos

3. **Mensaje de Acción Clínica**
   - Destacado con iconos y colores
   - Texto grande y legible
   - Recomendaciones claras

4. **Detalles Adicionales**
   - Probabilidad exacta
   - Fecha y hora de evaluación
   - Tipo de acción requerida

## 🎯 Validaciones Implementadas

### Validación Frontend (JavaScript)

```javascript
// Rangos numéricos validados
const validations = {
    age: { min: 0, max: 120 },
    bmi: { min: 10, max: 60 },
    liver_function_score: { min: 0, max: 100 },
    alpha_fetoprotein_level: { min: 0, max: 1000 }
};

// Validación automática en inputs
input.addEventListener('input', function() {
    if (value < min) this.value = min;
    if (value > max) this.value = max;
});
```

### Validación en Campos de Selección

```javascript
// Valores válidos
const validValues = {
    gender: ['Male', 'Female'],
    alcohol_consumption: ['Never', 'Occasional', 'Regular'],
    smoking_status: ['Never', 'Former', 'Current'],
    physical_activity_level: ['Low', 'Moderate', 'High']
};
```

## 🎨 Paleta de Colores

```css
:root {
    /* Colores principales */
    --primary-color: #0066cc;      /* Azul médico */
    --primary-dark: #0052a3;       /* Azul oscuro */
    --primary-light: #e6f0ff;      /* Azul claro */
    
    /* Estados */
    --success-color: #28a745;      /* Verde (bajo riesgo) */
    --warning-color: #ffc107;      /* Amarillo (advertencia) */
    --danger-color: #dc3545;       /* Rojo (alto riesgo) */
    
    /* Texto y fondos */
    --text-primary: #2c3e50;
    --text-secondary: #6c757d;
    --bg-primary: #ffffff;
    --bg-secondary: #f8f9fa;
}
```

## 📊 Animaciones y Efectos

### 1. **Animación de Carga**
```javascript
// Barra de progreso animada
// Mensajes cambiantes durante la carga:
// - "Analizando datos del paciente..."
// - "Procesando información clínica..."
// - "Evaluando factores de riesgo..."
```

### 2. **Animación de Resultados**
```javascript
// 1. Fade in del contenedor
// 2. Animación numérica del porcentaje
// 3. Animación del círculo SVG
// 4. Animación del marcador del gauge
// 5. Aparición del mensaje de acción
```

### 3. **Transiciones Suaves**
- Todos los cambios de estado son animados
- Transiciones CSS de 0.3s en elementos interactivos
- Scroll suave a secciones relevantes

## 📱 Características de Accesibilidad

### ARIA Labels
```html
<input type="number" 
       aria-label="Edad del paciente"
       aria-required="true">
```

### Navegación por Teclado
- Todos los elementos son accesibles con Tab
- Enter para enviar formulario
- Orden lógico de tabulación

### Reducción de Movimiento
```css
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}
```

## 🔧 Funcionalidades Adicionales

### 1. **Descarga de Resultados**
```javascript
// Botón para descargar reporte en formato TXT
downloadResults() {
    // Genera archivo con:
    // - Fecha de evaluación
    // - Porcentaje de riesgo
    // - Recomendación clínica
    // - Aviso legal
}
```

### 2. **Impresión de Resultados**
```javascript
// Estilos optimizados para impresión
window.print()
```

### 3. **Notificaciones**
```javascript
// Sistema de notificaciones toast
showNotification('Mensaje', 'success')
// Tipos: success, info, warning, error
```

## 🎯 Flujo de Usuario

1. **Ingreso de Datos**
   - Usuario completa formulario sección por sección
   - Validación en tiempo real
   - Ayudas contextuales

2. **Envío de Datos**
   - Click en "Evaluar Riesgo"
   - Mostrar loader y barra de progreso
   - Mensajes informativos de procesamiento

3. **Recepción de Resultados**
   - Ocultar loader
   - Animar aparición de resultados
   - Scroll automático a resultados

4. **Acciones Post-Resultados**
   - Ver resultados detallados
   - Imprimir reporte
   - Descargar reporte
   - Nueva evaluación

## 📐 Estructura de Archivos Frontend

```
frontend/
├── index.html          # Estructura HTML5 semántica
├── styles.css          # Estilos CSS3 con variables y responsive
└── script.js           # Lógica JavaScript moderna (ES6+)
```

## 🚀 Mejores Prácticas Implementadas

### HTML
✅ Semántica correcta (header, main, section, form)  
✅ Atributos ARIA para accesibilidad  
✅ Meta tags para SEO y responsive  
✅ Estructura organizada y comentada  

### CSS
✅ Variables CSS para mantenibilidad  
✅ Mobile-first design  
✅ Grid y Flexbox para layouts  
✅ Animaciones CSS3 performantes  
✅ Media queries para todos los dispositivos  

### JavaScript
✅ Código modular y reutilizable  
✅ Async/await para llamadas API  
✅ Manejo completo de errores  
✅ Validación exhaustiva  
✅ Comentarios descriptivos  

## 🎨 Personalización

### Cambiar colores principales:
```css
:root {
    --primary-color: #tu-color;
    --success-color: #tu-color;
    --danger-color: #tu-color;
}
```

### Cambiar URL de la API:
```javascript
const API_URL = 'https://tu-dominio.com/api';
```

### Ajustar animaciones:
```javascript
// En displayResults()
animateValue(element, 0, value, 1500); // Cambiar duración
```

## 🧪 Testing del Frontend

### Pruebas Manuales Recomendadas:

1. ✅ Probar en diferentes navegadores (Chrome, Firefox, Safari, Edge)
2. ✅ Probar en diferentes dispositivos (móvil, tablet, desktop)
3. ✅ Validar todos los campos del formulario
4. ✅ Probar con valores extremos (0, 100, 1000)
5. ✅ Verificar manejo de errores de red
6. ✅ Probar funcionalidad offline
7. ✅ Verificar accesibilidad con herramientas

### Herramientas Útiles:
- Chrome DevTools (Responsive Mode)
- Lighthouse (Auditoría de rendimiento)
- WAVE (Evaluación de accesibilidad)

## 📈 Optimizaciones de Rendimiento

✅ **Carga asíncrona** de recursos  
✅ **Lazy loading** de imágenes (si aplica)  
✅ **Minimización** de repaints/reflows  
✅ **Debouncing** en validaciones  
✅ **CSS eficiente** con especificidad baja  

## 🎓 Conclusión

El frontend está diseñado siguiendo las **mejores prácticas de UX/UI** con énfasis en:

- 🎯 **Usabilidad**: Fácil de usar para cualquier usuario
- 📱 **Accesibilidad**: Funciona en todos los dispositivos
- 🚀 **Rendimiento**: Carga rápida y animaciones fluidas
- 🔒 **Confiabilidad**: Validación exhaustiva y manejo de errores
- 🎨 **Diseño**: Profesional, moderno y médicamente apropiado

---

**¿Necesitas ayuda?** Consulta el `README.md` principal o revisa el código comentado en cada archivo.

