"""
Script de setup e inicialización del proyecto
Asegura que todas las dependencias y estructura estén correctas
"""

import os
import subprocess
import sys

def print_header(text):
    """Imprime un encabezado formateado"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_step(text):
    """Imprime un paso del proceso"""
    print(f"✓ {text}")

def check_python_version():
    """Verifica la versión de Python"""
    print_header("Verificando Versión de Python")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print_step(f"Python {version.major}.{version.minor}.{version.micro} ✓")
    return True

def check_directories():
    """Verifica que existan los directorios necesarios"""
    print_header("Verificando Estructura de Directorios")
    
    directories = [
        "data",
        "model",
        "backend",
        "backend/saved_models",
        "frontend"
    ]
    
    for dir_path in directories:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            print_step(f"Directorio creado: {dir_path}")
        else:
            print_step(f"Directorio existe: {dir_path}")
    
    return True

def check_data_files():
    """Verifica que existan los archivos de datos"""
    print_header("Verificando Archivos de Datos")
    
    if not os.path.exists("data/liver_cancer_data.csv"):
        print("⚠️  Archivo data/liver_cancer_data.csv no encontrado")
        print("   Ejecuta primero: python export_data.py")
        return False
    
    print_step("Archivo liver_cancer_data.csv encontrado")
    return True

def install_dependencies():
    """Instala las dependencias del proyecto"""
    print_header("Instalando Dependencias")
    
    # Instalar dependencias del modelo
    if os.path.exists("model/requirements.txt"):
        print_step("Instalando dependencias del modelo...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "model/requirements.txt"], 
                      check=False)
    
    # Instalar dependencias del backend
    if os.path.exists("backend/requirements.txt"):
        print_step("Instalando dependencias del backend...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"], 
                      check=False)
    
    print_step("Dependencias instaladas")
    return True

def check_model_trained():
    """Verifica si el modelo ya fue entrenado"""
    print_header("Verificando Modelo Entrenado")
    
    model_files = [
        "backend/saved_models/liver_cancer_model.keras",
        "backend/saved_models/scaler.pkl",
        "backend/saved_models/feature_metadata.json"
    ]
    
    all_exist = all(os.path.exists(f) for f in model_files)
    
    if all_exist:
        print_step("✓ Modelo entrenado encontrado")
        return True
    else:
        print("⚠️  Modelo no entrenado aún")
        print("   Para entrenar el modelo, ejecuta:")
        print("   cd model && python train_model.py")
        return False

def main():
    """Función principal de setup"""
    print("\n" + "="*60)
    print("  🏥 SETUP - Sistema de Predicción de Cáncer de Hígado")
    print("="*60)
    
    # 1. Verificar Python
    if not check_python_version():
        sys.exit(1)
    
    # 2. Verificar directorios
    check_directories()
    
    # 3. Verificar archivos de datos
    data_ready = check_data_files()
    
    # 4. Instalar dependencias
    install_dependencies()
    
    # 5. Verificar modelo
    model_ready = check_model_trained()
    
    # Resumen
    print_header("Resumen del Setup")
    
    print(f"✓ Estructura de directorios: OK")
    print(f"{'✓' if data_ready else '⚠'} Archivos de datos: {'OK' if data_ready else 'PENDIENTE'}")
    print(f"✓ Dependencias: OK")
    print(f"{'✓' if model_ready else '⚠'} Modelo entrenado: {'OK' if model_ready else 'PENDIENTE'}")
    
    if not data_ready:
        print("\n📋 Próximos pasos:")
        print("   1. python export_data.py")
        print("   2. cd model && python train_model.py")
        print("   3. cd backend && python app.py")
    elif not model_ready:
        print("\n📋 Próximos pasos:")
        print("   1. cd model && python train_model.py")
        print("   2. cd backend && python app.py")
    else:
        print("\n✅ ¡Setup completo! Puedes iniciar la aplicación:")
        print("   1. cd backend && python app.py")
        print("   2. Abrir frontend/index.html en el navegador")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()

