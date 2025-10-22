"""
Script de testing para la API de predicción de cáncer
Prueba diferentes escenarios y casos de uso
"""

import requests
import json
from datetime import datetime

# URL base de la API
API_URL = "http://localhost:5000"

# Colores para output en terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_test_header(test_name):
    """Imprime el encabezado de un test"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}TEST: {test_name}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")

def print_result(success, message):
    """Imprime el resultado de un test"""
    if success:
        print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")

def test_health_check():
    """Test del endpoint de health check"""
    print_test_header("Health Check")
    
    try:
        response = requests.get(f"{API_URL}/health")
        data = response.json()
        
        print_result(response.status_code == 200, f"Status code: {response.status_code}")
        print_result(data['status'] == 'healthy', f"Health status: {data['status']}")
        print_result(data['model_loaded'], "Modelo cargado")
        print_result(data['scaler_loaded'], "Scaler cargado")
        print_result(data['metadata_loaded'], "Metadata cargada")
        
        print(f"\n{Colors.OKCYAN}Response:{Colors.ENDC}")
        print(json.dumps(data, indent=2))
        
        return response.status_code == 200 and data['status'] == 'healthy'
        
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def test_api_info():
    """Test del endpoint raíz"""
    print_test_header("API Information")
    
    try:
        response = requests.get(f"{API_URL}/")
        data = response.json()
        
        print_result(response.status_code == 200, f"Status code: {response.status_code}")
        print_result('api' in data, "Información de API presente")
        print_result('endpoints' in data, "Lista de endpoints presente")
        
        print(f"\n{Colors.OKCYAN}Response:{Colors.ENDC}")
        print(json.dumps(data, indent=2))
        
        return response.status_code == 200
        
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def test_prediction_low_risk():
    """Test de predicción con paciente de bajo riesgo"""
    print_test_header("Predicción - Paciente de Bajo Riesgo")
    
    # Datos de un paciente típico de bajo riesgo
    patient_data = {
        "age": 35,
        "gender": "Female",
        "bmi": 22.5,
        "alcohol_consumption": "Never",
        "smoking_status": "Never",
        "physical_activity_level": "High",
        "liver_function_score": 85.0,
        "alpha_fetoprotein_level": 5.0,
        "hepatitis_b": 0,
        "hepatitis_c": 0,
        "cirrhosis_history": 0,
        "family_history_cancer": 0,
        "diabetes": 0
    }
    
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=patient_data,
            headers={'Content-Type': 'application/json'}
        )
        
        data = response.json()
        
        print_result(response.status_code == 200, f"Status code: {response.status_code}")
        print_result(data['success'], "Predicción exitosa")
        
        if data['success']:
            risk = data['prediction']['risk_percentage']
            print_result(risk <= 50, f"Riesgo bajo esperado: {risk}%")
            print_result(
                data['prediction']['risk_message'] == "Recomendación de seguimiento/chequeos.",
                "Mensaje de acción correcto"
            )
        
        print(f"\n{Colors.OKCYAN}Request:{Colors.ENDC}")
        print(json.dumps(patient_data, indent=2))
        
        print(f"\n{Colors.OKCYAN}Response:{Colors.ENDC}")
        print(json.dumps(data, indent=2))
        
        return response.status_code == 200 and data['success']
        
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def test_prediction_high_risk():
    """Test de predicción con paciente de alto riesgo"""
    print_test_header("Predicción - Paciente de Alto Riesgo")
    
    # Datos de un paciente típico de alto riesgo
    patient_data = {
        "age": 65,
        "gender": "Male",
        "bmi": 32.0,
        "alcohol_consumption": "Regular",
        "smoking_status": "Current",
        "physical_activity_level": "Low",
        "liver_function_score": 45.0,
        "alpha_fetoprotein_level": 250.0,
        "hepatitis_b": 1,
        "hepatitis_c": 1,
        "cirrhosis_history": 1,
        "family_history_cancer": 1,
        "diabetes": 1
    }
    
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=patient_data,
            headers={'Content-Type': 'application/json'}
        )
        
        data = response.json()
        
        print_result(response.status_code == 200, f"Status code: {response.status_code}")
        print_result(data['success'], "Predicción exitosa")
        
        if data['success']:
            risk = data['prediction']['risk_percentage']
            print_result(risk > 50, f"Riesgo alto esperado: {risk}%")
            print_result(
                data['prediction']['risk_message'] == "Alerta: Cita clínica inmediata.",
                "Mensaje de acción correcto"
            )
        
        print(f"\n{Colors.OKCYAN}Request:{Colors.ENDC}")
        print(json.dumps(patient_data, indent=2))
        
        print(f"\n{Colors.OKCYAN}Response:{Colors.ENDC}")
        print(json.dumps(data, indent=2))
        
        return response.status_code == 200 and data['success']
        
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def test_invalid_data():
    """Test con datos inválidos"""
    print_test_header("Datos Inválidos")
    
    # Datos con campos faltantes
    invalid_data = {
        "age": 150,  # Edad fuera de rango
        "gender": "Unknown",  # Género inválido
        "bmi": 22.5
        # Faltan muchos campos requeridos
    }
    
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=invalid_data,
            headers={'Content-Type': 'application/json'}
        )
        
        data = response.json()
        
        print_result(response.status_code == 400, f"Status code esperado 400: {response.status_code}")
        print_result('error' in data, "Mensaje de error presente")
        
        print(f"\n{Colors.OKCYAN}Request:{Colors.ENDC}")
        print(json.dumps(invalid_data, indent=2))
        
        print(f"\n{Colors.OKCYAN}Response:{Colors.ENDC}")
        print(json.dumps(data, indent=2))
        
        return response.status_code == 400
        
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def test_features_endpoint():
    """Test del endpoint de features"""
    print_test_header("Features Information")
    
    try:
        response = requests.get(f"{API_URL}/features")
        data = response.json()
        
        print_result(response.status_code == 200, f"Status code: {response.status_code}")
        print_result('features' in data, "Lista de features presente")
        print_result('encoders' in data, "Encoders presentes")
        print_result('feature_info' in data, "Información de features presente")
        
        print(f"\n{Colors.OKCYAN}Features esperadas:{Colors.ENDC}")
        for feature in data.get('features', []):
            print(f"  - {feature}")
        
        return response.status_code == 200
        
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def test_edge_cases():
    """Test de casos límite"""
    print_test_header("Casos Límite")
    
    # Caso con valores en los límites
    edge_case_data = {
        "age": 0,  # Edad mínima
        "gender": "Male",
        "bmi": 60.0,  # IMC máximo
        "alcohol_consumption": "Never",
        "smoking_status": "Never",
        "physical_activity_level": "Low",
        "liver_function_score": 100.0,  # Puntuación máxima
        "alpha_fetoprotein_level": 0.0,  # Nivel mínimo
        "hepatitis_b": 0,
        "hepatitis_c": 0,
        "cirrhosis_history": 0,
        "family_history_cancer": 0,
        "diabetes": 0
    }
    
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=edge_case_data,
            headers={'Content-Type': 'application/json'}
        )
        
        data = response.json()
        
        print_result(response.status_code == 200, f"Status code: {response.status_code}")
        print_result(data['success'], "Predicción con valores límite exitosa")
        
        if data['success']:
            risk = data['prediction']['risk_percentage']
            print_result(0 <= risk <= 100, f"Riesgo en rango válido: {risk}%")
        
        print(f"\n{Colors.OKCYAN}Response:{Colors.ENDC}")
        print(json.dumps(data, indent=2))
        
        return response.status_code == 200 and data['success']
        
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def run_all_tests():
    """Ejecuta todos los tests"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}🧪 INICIANDO SUITE DE TESTS DE LA API{Colors.ENDC}")
    print(f"{Colors.BOLD}Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
    print(f"{Colors.BOLD}API URL: {API_URL}{Colors.ENDC}")
    
    tests = [
        ("Health Check", test_health_check),
        ("API Info", test_api_info),
        ("Predicción Bajo Riesgo", test_prediction_low_risk),
        ("Predicción Alto Riesgo", test_prediction_high_risk),
        ("Datos Inválidos", test_invalid_data),
        ("Features Endpoint", test_features_endpoint),
        ("Casos Límite", test_edge_cases)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n{Colors.FAIL}Error ejecutando test {test_name}: {str(e)}{Colors.ENDC}")
            results.append((test_name, False))
    
    # Resumen de resultados
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}RESUMEN DE RESULTADOS{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = f"{Colors.OKGREEN}PASSED{Colors.ENDC}" if success else f"{Colors.FAIL}FAILED{Colors.ENDC}"
        print(f"{test_name:<30} {status}")
    
    print(f"\n{Colors.BOLD}Total: {passed}/{total} tests pasados ({(passed/total)*100:.1f}%){Colors.ENDC}")
    
    if passed == total:
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}✅ ¡Todos los tests pasaron exitosamente!{Colors.ENDC}")
    else:
        print(f"\n{Colors.WARNING}{Colors.BOLD}⚠️ Algunos tests fallaron. Revise los detalles arriba.{Colors.ENDC}")

if __name__ == "__main__":
    try:
        # Verificar conexión básica
        print(f"{Colors.BOLD}Verificando conexión con la API...{Colors.ENDC}")
        response = requests.get(f"{API_URL}/health", timeout=5)
        print(f"{Colors.OKGREEN}✓ API disponible{Colors.ENDC}")
        
        # Ejecutar todos los tests
        run_all_tests()
        
    except requests.exceptions.ConnectionError:
        print(f"\n{Colors.FAIL}{Colors.BOLD}❌ ERROR: No se puede conectar con la API en {API_URL}{Colors.ENDC}")
        print(f"{Colors.WARNING}Asegúrese de que el servidor Flask esté ejecutándose:{Colors.ENDC}")
        print(f"  cd backend")
        print(f"  python app.py")
    except Exception as e:
        print(f"\n{Colors.FAIL}{Colors.BOLD}❌ ERROR inesperado: {str(e)}{Colors.ENDC}")
