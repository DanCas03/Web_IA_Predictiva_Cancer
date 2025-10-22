# 🏥 Sistema de Predicción de Riesgo de Cáncer de Hígado

Una aplicación completa de predicción de riesgo de cáncer utilizando Deep Learning (MLP), con backend Flask y frontend web moderno.

## 📋 Descripción

Este sistema utiliza una Red Neuronal Multicapa (MLP) para predecir la probabilidad de riesgo de cáncer de hígado en pacientes basándose en 13 características clínicas y de estilo de vida. La aplicación consta de:

- **Modelo de Deep Learning**: Red neuronal entrenada con TensorFlow/Keras
- **API REST**: Backend Flask que sirve las predicciones
- **WebApp**: Interfaz de usuario moderna con HTML/CSS/JavaScript

## 🚀 Características

### Modelo y Predicción
- ✅ Red Neuronal Multicapa (MLP) con TensorFlow/Keras
- ✅ Predicción de riesgo en tiempo real (0-100%)
- ✅ Precisión del modelo: ~85-90%
- ✅ 13 características clínicas analizadas

### Frontend Avanzado
- ✅ **Interfaz Intuitiva**: Diseño moderno con UX optimizada
- ✅ **100% Responsive**: Funciona en móviles, tablets y desktop
- ✅ **Visualización Avanzada**: Círculos SVG animados y gauges interactivos
- ✅ **Animaciones Fluidas**: Transiciones y efectos profesionales
- ✅ **Validación en Tiempo Real**: Feedback inmediato al usuario
- ✅ **Accesibilidad**: Soporte ARIA y navegación por teclado
- ✅ **Modo de impresión**: Estilos optimizados para reportes

### Backend y API
- ✅ API REST con Flask y CORS
- ✅ Validación exhaustiva de datos
- ✅ Mensajes de acción clínicos claros
- ✅ Health checks y monitoreo
- ✅ Documentación completa de endpoints

### Características Adicionales
- ✅ Descarga de reportes en formato texto
- ✅ Notificaciones en tiempo real
- ✅ Barra de progreso con mensajes informativos
- ✅ Soporte para modo oscuro (preferencia del sistema)

## 📁 Estructura del Proyecto

```
proyecto/
│
├── synthetic_liver_cancer_dataset.sql   # Dataset original
├── export_data.py                       # Script para exportar SQL a CSV
├── README.md                            # Este archivo
├── test_api.py                          # Script de testing
│
├── data/                                # Datos procesados
│   └── liver_cancer_data.csv
│
├── model/                               # Código del modelo
│   ├── train_model.py                   # Script de entrenamiento
│   ├── requirements.txt                 # Dependencias del modelo
│   ├── training_history.png             # Gráfico del entrenamiento
│   ├── confusion_matrix.png             # Matriz de confusión
│   └── roc_curve.png                   # Curva ROC
│
├── backend/                             # API Flask
│   ├── app.py                          # Aplicación Flask
│   ├── requirements.txt                # Dependencias del backend
│   └── saved_models/                   # Modelos guardados
│       ├── liver_cancer_model.h5       # Modelo entrenado
│       ├── scaler.pkl                  # Escalador
│       └── feature_metadata.json       # Metadata de features
│
└── frontend/                            # WebApp
    ├── index.html                      # Página principal
    ├── styles.css                      # Estilos
    └── script.js                       # Lógica JavaScript
```

## 🛠️ Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Navegador web moderno (Chrome, Firefox, Edge)

### Paso 1: Clonar o Descargar el Proyecto

```bash
cd proyecto
```

### Paso 2: Exportar Datos de SQL a CSV

```bash
python export_data.py
```

Esto creará el archivo `data/liver_cancer_data.csv` con los datos procesados.

### Paso 3: Entrenar el Modelo

```bash
# Navegar al directorio del modelo
cd model

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Entrenar el modelo
python train_model.py

# Volver al directorio principal
cd ..
```

### Paso 4: Configurar y Ejecutar el Backend

```bash
# Navegar al directorio del backend
cd backend

# Crear entorno virtual (si no está usando el mismo del modelo)
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la API Flask
python app.py
```

La API estará disponible en `http://localhost:5000`

### Paso 5: Abrir la Aplicación Web

1. Mantener el servidor Flask ejecutándose
2. Abrir el archivo `frontend/index.html` en un navegador web
3. O servir los archivos frontend con un servidor web local:

```bash
# Si tienes Python instalado
cd frontend
python -m http.server 8080

# Luego abrir http://localhost:8080 en el navegador
```

## 📊 Uso de la Aplicación

### 1. Completar el Formulario

La interfaz guía al usuario a través de 4 secciones organizadas:

#### 📋 **Información Demográfica**
- Edad (0-120 años)
- Género (Masculino/Femenino)
- IMC - Índice de Masa Corporal (10-60 kg/m²)

#### 🏃 **Estilo de Vida**
- Consumo de Alcohol (Nunca/Ocasional/Regular)
- Estado de Fumador (Nunca/Ex-fumador/Fumador actual)
- Nivel de Actividad Física (Bajo/Moderado/Alto)

#### 🔬 **Indicadores Clínicos**
- Puntuación de Función Hepática (0-100)
- Nivel de Alfa-fetoproteína (0-1000 ng/mL)

#### 🏥 **Condiciones Médicas**
- Hepatitis B (Sí/No)
- Hepatitis C (Sí/No)
- Historial de Cirrosis (Sí/No)
- Historial Familiar de Cáncer (Sí/No)
- Diabetes (Sí/No)

**Validación Automática**: Todos los campos se validan en tiempo real.

### 2. Obtener Predicción

Al hacer clic en **"Evaluar Riesgo"**:

1. 🔄 **Barra de Progreso Animada** con mensajes informativos:
   - "Analizando datos del paciente..."
   - "Procesando información clínica..."
   - "Evaluando factores de riesgo..."
   - "Calculando probabilidad..."
   - "Generando recomendaciones..."

2. ⏱️ **Tiempo de respuesta**: ~2-3 segundos

3. 📊 **Resultados Visuales**:
   - **Círculo SVG Animado**: Muestra el porcentaje visualmente
   - **Número Grande**: Porcentaje de riesgo destacado
   - **Gauge Interactivo**: Barra con marcador de posición
   - **Código de Colores**: Verde (bajo) / Rojo (alto)

### 3. Interpretar Resultados

Los resultados incluyen **5 componentes visuales**:

#### 🎯 **Indicador Principal**
- Porcentaje de riesgo en números grandes
- Etiqueta: "RIESGO BAJO" o "RIESGO ALTO"
- Animación de conteo desde 0% hasta el valor final

#### 📊 **Gauge de Riesgo**
- Barra horizontal dividida en zonas:
  - Verde: 0-50% (Bajo Riesgo)
  - Rojo: 51-100% (Alto Riesgo)
- Marcador animado que indica posición exacta

#### 💬 **Recomendación Clínica**
- **Riesgo Bajo (0-50%)**:  
  ✅ "Recomendación de seguimiento/chequeos."
  
- **Riesgo Alto (51-100%)**:  
  🚨 "Alerta: Cita clínica inmediata."

#### 📋 **Detalles Adicionales**
- Probabilidad exacta (decimal)
- Fecha y hora de la evaluación
- Tipo de acción requerida

#### 🛠️ **Acciones Disponibles**
- 📄 **Imprimir**: Genera versión imprimible del reporte
- 💾 **Guardar PDF**: Descarga reporte en formato texto
- 🔄 **Nueva Evaluación**: Reinicia el formulario

### 4. Características de Accesibilidad

- ♿ **Navegación por teclado** completa
- 📱 **Responsive** en todos los dispositivos
- 🎨 **Alto contraste** para mejor legibilidad
- 📖 **Etiquetas ARIA** para lectores de pantalla
- ⏸️ **Respeto a preferencias** de movimiento reducido

## 🔌 API REST - Documentación

### Endpoints Disponibles

#### `GET /`
Información básica de la API

#### `GET /health`
Verificación del estado de la API

**Respuesta ejemplo:**
```json
{
    "status": "healthy",
    "timestamp": "2024-01-15T10:30:00",
    "model_loaded": true,
    "scaler_loaded": true,
    "metadata_loaded": true
}
```

#### `POST /predict`
Endpoint principal de predicción

**Request Body:**
```json
{
    "age": 55,
    "gender": "Male",
    "bmi": 28.5,
    "alcohol_consumption": "Regular",
    "smoking_status": "Former",
    "physical_activity_level": "Moderate",
    "liver_function_score": 65.5,
    "alpha_fetoprotein_level": 15.3,
    "hepatitis_b": 0,
    "hepatitis_c": 0,
    "cirrhosis_history": 1,
    "family_history_cancer": 1,
    "diabetes": 0
}
```

**Response:**
```json
{
    "success": true,
    "prediction": {
        "risk_percentage": 67.5,
        "risk_probability": 0.675,
        "risk_level": "alto",
        "risk_message": "Alerta: Cita clínica inmediata.",
        "action_required": "immediate"
    },
    "timestamp": "2024-01-15T10:30:00"
}
```

#### `GET /features`
Obtener información sobre las features esperadas

## 🧪 Testing

Ejecute el script de pruebas para verificar la API:

```bash
python test_api.py
```

## 📈 Rendimiento del Modelo

Los resultados del entrenamiento se guardan en el directorio `model/`:

- `training_history.png`: Evolución del entrenamiento
- `confusion_matrix.png`: Matriz de confusión
- `roc_curve.png`: Curva ROC y AUC

Métricas típicas esperadas:
- Accuracy: ~85-90%
- AUC: ~0.88-0.92

## ⚠️ Aviso Legal

**IMPORTANTE**: Esta herramienta es solo para fines de evaluación preliminar y educativos. NO reemplaza el diagnóstico médico profesional. Siempre consulte con un médico especialista para obtener un diagnóstico definitivo.

## 🐛 Solución de Problemas

### Error: "No se puede conectar con el servidor"
- Verificar que el backend Flask esté ejecutándose
- Verificar que esté usando el puerto correcto (5000)
- Desactivar temporalmente el firewall si es necesario

### Error: "Modelo no encontrado"
- Asegurarse de haber ejecutado `train_model.py` primero
- Verificar que los archivos estén en `backend/saved_models/`

### Error: "Datos inválidos"
- Verificar que todos los campos del formulario estén completos
- Revisar los rangos válidos para cada campo

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Cree una rama para su feature (`git checkout -b feature/AmazingFeature`)
3. Commit sus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abra un Pull Request

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la Licencia MIT.

## 👥 Autor

Desarrollado con ❤️ utilizando Python, TensorFlow, Flask y tecnologías web modernas.

---

*Última actualización: Enero 2024*
