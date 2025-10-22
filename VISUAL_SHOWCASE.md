# 🎨 Showcase Visual del Frontend

## Vista General de la Aplicación

Este documento describe la apariencia visual y la experiencia de usuario de la aplicación.

---

## 📱 Pantalla Principal - Formulario

### Headerv
```
╔═══════════════════════════════════════════════════════════════╗
║																║
║								🏥								║
║		Sistema de Predicción de Riesgo de Cáncer de Hígado		║
║		Evaluación Basada en Inteligencia Artificial y Deep		║
║							Learning							║
║																║
║  [IA Avanzada]  [Predicción en Tiempo Real]  [Resultados]		║
║							[Instantáneos]						║
║																║
╚═══════════════════════════════════════════════════════════════╝
```
- Fondo: Gradiente azul (#0066cc → #003366)
- Texto: Blanco con sombra
- Animación: Icono con efecto pulse

### Formulario - Sección 1: Información Demográfica
```
┌───────────────────────────────────────────────────────────┐
│	Información Demográfica									│
├───────────────────────────────────────────────────────────┤
│															│
│	Edad			Género				IMC					│
│	[____]			[▼ Masculino]		[____]				│
│	Años (0-120)	Seleccionar...		kg/m² (10-60)		│
│															│
└───────────────────────────────────────────────────────────┘
```

### Formulario - Sección 2: Estilo de Vida
```
┌───────────────────────────────────────────────────────────┐
│ Estilo de Vida											│
├───────────────────────────────────────────────────────────┤
│															│
│	Consumo de Alcohol	Estado Fumador	Actividad Física	│
│	[▼ Nunca]			[▼ Nunca]		[▼ Bajo]			│
│															│
└───────────────────────────────────────────────────────────┘
```

### Formulario - Sección 3: Indicadores Clínicos
```
┌───────────────────────────────────────────────────────────┐
│ Indicadores Clínicos										│
├───────────────────────────────────────────────────────────┤
│															│
│	Puntuación Función Hepática		Nivel Alfa-fetoproteína	│
│	[____]							[____]					│
│	0-100 puntos					ng/mL (0-1000)			│
│															│
└───────────────────────────────────────────────────────────┘
```

### Formulario - Sección 4: Condiciones Médicas
```
┌───────────────────────────────────────────────────────────┐
│ Condiciones Médicas										│
├───────────────────────────────────────────────────────────┤
│															│
│  ☐ Hepatitis B         ☐ Hepatitis C						│
│  ☐ Historial Cirrosis  ☐ Historial Familiar Cáncer		│
│  ☐ Diabetes												│
│															│
└───────────────────────────────────────────────────────────┘
```

### Botones de Acción
```
┌───────────────────────────────────────────────────────────┐
│															│
│		┌──────────────────┐	┌───────────────────┐		│
│		│ Evaluar Riesgo   │	│ Limpiar Formulario│		│
│		└──────────────────┘	└───────────────────┘		│
│															│
└───────────────────────────────────────────────────────────┘
```
- Botón principal: Azul (#0066cc)
- Botón secundario: Borde azul, fondo transparente
- Hover: Elevación y sombra

---

## ⏳ Durante el Procesamiento

### Barra de Progreso Animada
```
┌───────────────────────────────────────────────────────────┐
│															│
│	████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░	│
│															│
│			Analizando datos del paciente...				│
│															│
└───────────────────────────────────────────────────────────┘
```
- Color: Gradiente azul animado
- Mensajes cambiantes cada 400ms
- Altura: 6px con bordes redondeados

---

## 📊 Pantalla de Resultados

### Resultado - Riesgo BAJO (0-50%)

```
╔═══════════════════════════════════════════════════════════════╗
║																║
║	📊	Resultado de la Evaluación								║
║																║
║							  ⭕								║
║							  ◢◣								║
║						   ◢ 35.7 ◣								║
║						  ◢   %   ◣								║
║						  ◢═══════◣								║
║																║
║						  RIESGO BAJO							║
║						Nivel de Riesgo							║
║																║
╠═══════════════════════════════════════════════════════════════╣
║																║
║	Escala de Riesgo											║
║	▼															║
║	[████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]		║
║	● Bajo (0-50%)			● Alto (51-100%)					║
║																║
╠═══════════════════════════════════════════════════════════════╣
║																║
║		✅  Recomendación Clínica								║
║																║
║		Recomendación de seguimiento/chequeos.					║
║																║
╠═══════════════════════════════════════════════════════════════╣
║																║
║  Probabilidad: 0.3570											║
║  Fecha: 22 de octubre de 2024, 14:30							║
║  Acción Requerida: Preventiva									║
║																║
╠═══════════════════════════════════════════════════════════════╣
║																║
║	[📄 Imprimir]	[💾 Guardar PDF]	[🔄 Nueva Evaluación]	║
║																║
╚═══════════════════════════════════════════════════════════════╝
```

**Colores Riesgo Bajo:**
- Círculo: Verde (#28a745)
- Texto: Verde
- Borde del mensaje: Verde
- Icono: ✅

---

### Resultado - Riesgo ALTO (51-100%)

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║  📊  Resultado de la Evaluación                              ║
║                                                               ║
║                        ⭕                                     ║
║                       ◢◣                                      ║
║                      ◢ 78.3 ◣                               ║
║                     ◢   %   ◣                               ║
║                    ◢═══════◣                                ║
║                                                               ║
║                   RIESGO ALTO                                ║
║                  Nivel de Riesgo                             ║
║                                                               ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  Escala de Riesgo                                            ║
║                                                    ▼          ║
║  [░░░░░░░░░░░░░░░░░░░░░░░░░░░░████████████████████████]     ║
║  ● Bajo (0-50%)              ● Alto (51-100%)               ║
║                                                               ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║        🚨  Recomendación Clínica                            ║
║                                                               ║
║         Alerta: Cita clínica inmediata.                     ║
║                                                               ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  Probabilidad: 0.7830                                        ║
║  Fecha: 22 de octubre de 2024, 14:30                        ║
║  Acción Requerida: Inmediata                                 ║
║                                                               ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  [📄 Imprimir] [💾 Guardar PDF] [🔄 Nueva Evaluación]      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

**Colores Riesgo Alto:**
- Círculo: Rojo (#dc3545)
- Texto: Rojo
- Borde del mensaje: Rojo
- Icono: 🚨

---

## 📱 Vista Móvil (< 480px)

```
┌────────────────────────┐
│         🏥             │
│   Sistema Predicción   │
│   Cáncer de Hígado    │
│                        │
│  [IA Avanzada]         │
│  [Predicción RT]       │
│  [Resultados]          │
├────────────────────────┤
│                        │
│ Información            │
│ Demográfica            │
│                        │
│ Edad                   │
│ [____]                 │
│ Años (0-120)           │
│                        │
│ Género                 │
│ [▼ Masculino      ▼]   │
│                        │
│ IMC                    │
│ [____]                 │
│ kg/m² (10-60)          │
│                        │
├────────────────────────┤
│ [Evaluar Riesgo]       │
│ [Limpiar]              │
└────────────────────────┘
```

**Adaptaciones Móvil:**
- Una columna para todos los elementos
- Botones a ancho completo
- Texto más pequeño pero legible
- Espaciado reducido
- Badges en columna

---

## 🎨 Elementos de Diseño Detallados

### Círculo SVG de Progreso

**Visualización técnica:**
```
     Radio: 85px
     Stroke: 15px
     ┌─────────────┐
     │     ████    │  
     │   ███░░███  │  <- Progreso animado
     │  ███░75%███ │  <- Porcentaje centrado
     │  ███░░░░███ │
     │   ████████  │
     └─────────────┘
```

**Animación:**
1. Inicio: stroke-dashoffset = 534.07 (círculo vacío)
2. Final: stroke-dashoffset según porcentaje
3. Duración: 1.5 segundos
4. Easing: ease-in-out

### Gauge de Riesgo

```
Escala de Riesgo
      ▼ (Marcador animado)
[════════════════════════════════════════]
├──────────────┼──────────────────────────┤
0%           50%                       100%
 Verde         Rojo
```

**Características:**
- Altura: 40px
- Gradiente: Verde → Rojo en 50%
- Marcador: 4px de ancho, 60px de altura
- Animación: left transition 1s

### Mensaje de Acción

**Riesgo Bajo:**
```
┌─────────────────────────────────────────┐
│                                         │
│  ✅  Recomendación Clínica              │
│                                         │
│  Recomendación de seguimiento/chequeos │
│                                         │
└─────────────────────────────────────────┘
```
- Fondo: rgba(40, 167, 69, 0.1)
- Borde: 2px solid #28a745

**Riesgo Alto:**
```
┌───────────────────────────────────────┐
│										│
│	🚨  Recomendación Clínica			│
│										│
│	Alerta: Cita clínica inmediata		│
│										│
└───────────────────────────────────────┘
```
- Fondo: rgba(220, 53, 69, 0.1)
- Borde: 2px solid #dc3545

---

## 🎬 Secuencia de Animaciones

### Timeline de Resultados (4 segundos totales)

```
0.0s ─────────────────────────────────────> 4.0s

├─ 0.0s: Fade in contenedor (0.6s)
│
├─ 0.2s: Inicio animaciones
│   ├─ Animación numérica (1.5s)
│   ├─ Animación círculo SVG (1.5s)
│   └─ Animación marcador gauge (1.0s)
│
├─ 0.7s: Fade in mensaje acción (0.8s)
│
└─ 1.7s: Animaciones completadas
```

### Estados Visuales del Botón

```
Normal:   [  Evaluar Riesgo  ]  <- Azul
Hover:    [  Evaluar Riesgo  ]  <- Azul oscuro + elevación
Active:   [  Evaluar Riesgo  ]  <- Presionado
Loading:  [ ⏳ Procesando... ]  <- Deshabilitado
```

---

## 🎯 Notificaciones Toast

```
Esquina Superior Derecha:
┌───────────────────────────┐
│ ✓ Reporte descargado		│
│	exitosamente			│
└───────────────────────────┘
```

**Características:**
- Posición: fixed, top: 20px, right: 20px
- Animación entrada: slideIn (0.3s)
- Duración: 3 segundos
- Animación salida: fadeOut (0.3s)
- Colores: Verde (success), Azul (info)

---

## 🌓 Modo Oscuro (Automático)

```
Sistema detecta preferencia → Activa colores oscuros

Cambios:
- Fondo: #1e1e1e
- Texto: #e0e0e0
- Bordes: #404040
- Cards: #2a2a2a
```

---

## ♿ Accesibilidad Visual

### Alto Contraste
- Todos los textos cumplen WCAG AA (4.5:1)
- Títulos cumplen AAA (7:1)

### Indicadores Visuales
- Focus: Anillo azul de 3px
- Error: Borde rojo + mensaje
- Éxito: Borde verde + icono

### Tamaños Mínimos
- Botones: 44x44px (área táctil)
- Texto body: 16px
- Texto pequeño: 14px mínimo

---

## 📐 Especificaciones Técnicas

### Colores Principales
```
--primary-color:     #0066cc  ████
--primary-dark:      #0052a3  ████
--success-color:     #28a745  ████
--danger-color:      #dc3545  ████
--warning-color:     #ffc107  ████
--text-primary:      #2c3e50  ████
--bg-primary:        #ffffff  ████
```

### Tipografía
```
Font Family: 'Inter', sans-serif
Pesos: 300, 400, 500, 600, 700, 800

Títulos:     2.5em / 700
Subtítulos:  1.8em / 600
Cuerpo:      1em   / 400
Pequeño:     0.9em / 400
```

### Espaciado
```
Container:    max-width: 1200px
Padding:      20-50px según sección
Gap:          15-20px entre elementos
Margin:       30-40px entre secciones
```

### Sombras
```
--shadow-sm:  0 2px 4px rgba(0,0,0,0.1)
--shadow-md:  0 4px 8px rgba(0,0,0,0.15)
--shadow-lg:  0 8px 16px rgba(0,0,0,0.2)
```

### Radios de Borde
```
--radius-sm:  4px  (inputs)
--radius-md:  8px  (cards)
--radius-lg:  12px (header, containers)
```

---

## 🎉 Resultado Final

Una interfaz **profesional, moderna y completamente funcional** que proporciona:

✅ Experiencia de usuario excepcional  
✅ Visualización clara y destacada de resultados  
✅ Adaptación perfecta a cualquier dispositivo  
✅ Animaciones fluidas y atractivas  
✅ Accesibilidad completa  
✅ Diseño médico apropiado  

**¡Lista para producción!** 🚀

