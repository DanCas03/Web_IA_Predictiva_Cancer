"""
API REST Flask para predicción de riesgo de cáncer de hígado
Sirve el modelo entrenado y maneja las solicitudes de predicción
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
import tensorflow as tf
import pickle
import json
import os
from datetime import datetime

# Inicializar Flask
app = Flask(__name__)
CORS(app)  # Habilitar CORS para permitir requests del frontend

# Variables globales para el modelo y preprocessors
model = None
scaler = None
feature_metadata = None
encoders = None

def load_model_artifacts():
	"""
	Carga el modelo, scaler y metadata al iniciar el servidor
	"""
	global model, scaler, feature_metadata, encoders
	
	try:
		# Cargar modelo Keras
		model_path = 'saved_models/liver_cancer_model.h5'
		model = tf.keras.models.load_model(model_path)
		print(f"Modelo cargado desde: {model_path}")
		
		# Cargar scaler
		scaler_path = 'saved_models/scaler.pkl'
		with open(scaler_path, 'rb') as f:
			scaler = pickle.load(f)
		print(f"Scaler cargado desde: {scaler_path}")
		
		# Cargar metadata
		metadata_path = 'saved_models/feature_metadata.json'
		with open(metadata_path, 'r') as f:
			feature_metadata = json.load(f)
		print(f"Metadata cargada desde: {metadata_path}")
		
		# Reconstruir encoders
		encoders = {}
		for col, classes in feature_metadata['encoders'].items():
			from sklearn.preprocessing import LabelEncoder
			le = LabelEncoder()
			le.classes_ = np.array(classes)
			encoders[col] = le
		
		print("Todos los artefactos del modelo cargados exitosamente")
		return True
		
	except Exception as e:
		print(f"Error cargando artefactos del modelo: {e}")
		return False

def validate_input_data(data):
	"""
	Valida que los datos de entrada tengan todas las features necesarias
	"""
	required_features = feature_metadata['feature_names']
	missing_features = [f for f in required_features if f not in data]
	
	if missing_features:
		return False, f"Faltan las siguientes características: {', '.join(missing_features)}"
	
	# Validar tipos de datos
	numeric_features = ['age', 'bmi', 'liver_function_score', 'alpha_fetoprotein_level']
	categorical_features = ['gender', 'alcohol_consumption', 'smoking_status', 'physical_activity_level']
	binary_features = ['hepatitis_b', 'hepatitis_c', 'cirrhosis_history', 'family_history_cancer', 'diabetes']
	
	# Validar rangos numéricos
	validations = {
		'age': (0, 120),
		'bmi': (10, 60),
		'liver_function_score': (0, 100),
		'alpha_fetoprotein_level': (0, 1000)
	}
	
	for feature, (min_val, max_val) in validations.items():
		if feature in data:
			value = float(data[feature])
			if not (min_val <= value <= max_val):
				return False, f"{feature} debe estar entre {min_val} y {max_val}"
	
	# Validar valores categóricos
	for feature in categorical_features:
		if feature in data and feature in encoders:
			if data[feature] not in encoders[feature].classes_:
				valid_values = encoders[feature].classes_.tolist()
				return False, f"{feature} debe ser uno de: {valid_values}"
	
	return True, "Datos válidos"

def preprocess_input(data):
	"""
	Preprocesa los datos de entrada para que coincidan con el formato de entrenamiento
	"""
	# Crear DataFrame con una sola fila
	df = pd.DataFrame([data])
	
	# Asegurar el orden correcto de las columnas
	df = df[feature_metadata['feature_names']]
	
	# Codificar variables categóricas
	categorical_columns = ['gender', 'alcohol_consumption', 'smoking_status', 'physical_activity_level']
	
	for col in categorical_columns:
		if col in encoders:
			df[col] = encoders[col].transform(df[col])
	
	# Convertir tipos de datos
	numeric_columns = ['age', 'bmi', 'liver_function_score', 'alpha_fetoprotein_level']
	for col in numeric_columns:
		df[col] = pd.to_numeric(df[col])
	
	# Convertir binarias a int
	binary_columns = ['hepatitis_b', 'hepatitis_c', 'cirrhosis_history', 'family_history_cancer', 'diabetes']
	for col in binary_columns:
		df[col] = df[col].astype(int)
	
	# Escalar características
	df_scaled = scaler.transform(df)
	
	return df_scaled

@app.route('/', methods=['GET'])
def home():
	"""
	Endpoint raíz - información básica de la API
	"""
	return jsonify({
		'api': 'Liver Cancer Risk Prediction API',
		'version': '1.0',
		'endpoints': {
			'/': 'API information',
			'/health': 'Health check',
			'/predict': 'POST - Predict cancer risk'
		},
		'model_performance': feature_metadata.get('model_performance', {})
	})

@app.route('/health', methods=['GET'])
def health_check():
	"""
	Health check endpoint para verificar que la API esté funcionando
	"""
	health_status = {
		'status': 'healthy' if model is not None else 'unhealthy',
		'timestamp': datetime.now().isoformat(),
		'model_loaded': model is not None,
		'scaler_loaded': scaler is not None,
		'metadata_loaded': feature_metadata is not None
	}
	
	return jsonify(health_status), 200 if health_status['status'] == 'healthy' else 503

@app.route('/predict', methods=['POST'])
def predict():
	"""
	Endpoint principal de predicción
	Acepta datos del paciente y devuelve probabilidad de riesgo
	"""
	try:
		# 1. Recibir datos JSON
		if not request.is_json:
			return jsonify({
				'error': 'Content-Type debe ser application/json'
			}), 400
		
		data = request.get_json()
		
		# 2. Validar datos de entrada
		is_valid, message = validate_input_data(data)
		if not is_valid:
			return jsonify({
				'error': 'Datos inválidos',
				'message': message
			}), 400
		
		# 3. Preprocesar datos
		input_processed = preprocess_input(data)
		
		# 4. Realizar predicción
		prediction_proba = model.predict(input_processed, verbose=0)
		risk_probability = float(prediction_proba[0][0])
		risk_percentage = round(risk_probability * 100, 2)
		
		# 5. Generar mensaje de acción según el riesgo
		if risk_percentage <= 50:
			risk_message = "Recomendación de seguimiento/chequeos."
			risk_level = "bajo"
			action_required = "preventive"
		else:
			risk_message = "Alerta: Cita clínica inmediata."
			risk_level = "alto"
			action_required = "immediate"
		
		# 6. Preparar respuesta
		response = {
			'success': True,
			'prediction': {
				'risk_percentage': risk_percentage,
				'risk_probability': risk_probability,
				'risk_level': risk_level,
				'risk_message': risk_message,
				'action_required': action_required
			},
			'input_data': data,
			'timestamp': datetime.now().isoformat()
		}
		
		# Log de predicción (útil para auditoría)
		app.logger.info(f"Predicción realizada: {risk_percentage}% - {risk_level}")
		
		return jsonify(response), 200
		
	except Exception as e:
		app.logger.error(f"Error en predicción: {str(e)}")
		return jsonify({
			'success': False,
			'error': 'Error interno del servidor',
			'message': str(e)
		}), 500

@app.route('/features', methods=['GET'])
def get_features():
	"""
	Endpoint auxiliar para obtener información sobre las features esperadas
	"""
	if feature_metadata is None:
		return jsonify({'error': 'Metadata no disponible'}), 503
	
	return jsonify({
		'features': feature_metadata['feature_names'],
		'encoders': feature_metadata['encoders'],
		'feature_info': {
			'numeric': ['age', 'bmi', 'liver_function_score', 'alpha_fetoprotein_level'],
			'categorical': ['gender', 'alcohol_consumption', 'smoking_status', 'physical_activity_level'],
			'binary': ['hepatitis_b', 'hepatitis_c', 'cirrhosis_history', 'family_history_cancer', 'diabetes']
		}
	})

@app.errorhandler(404)
def not_found(error):
	"""
	Manejador de errores 404
	"""
	return jsonify({
		'error': 'Endpoint no encontrado',
		'message': 'Verifica la URL y el método HTTP'
	}), 404

@app.errorhandler(500)
def internal_error(error):
	"""
	Manejador de errores 500
	"""
	return jsonify({
		'error': 'Error interno del servidor',
		'message': 'Por favor, contacta al administrador'
	}), 500

# Configuración de logging
if __name__ == '__main__':
	import logging
	logging.basicConfig(
		level=logging.INFO,
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
	)
	
	# Cargar artefactos del modelo al iniciar
	if load_model_artifacts():
		print("\nAPI lista para recibir solicitudes")
		print("Ejecutando en http://localhost:5000")
		app.run(debug=True, host='0.0.0.0', port=5000)
	else:
		print("\nError: No se pudieron cargar los artefactos del modelo")
		print("Asegúrate de entrenar el modelo primero ejecutando: python ../model/train_model.py")
