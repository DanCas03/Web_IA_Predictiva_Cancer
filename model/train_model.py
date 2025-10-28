"""
Script de entrenamiento para el modelo de predicción de cáncer de hígado
Entrena una Red Neuronal Multicapa (MLP) usando TensorFlow/Keras con Keras Tuner
"""

import pandas as pd
import numpy as np
import json
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import keras_tuner as kt
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar semilla para reproducibilidad
seed = 42
np.random.seed(seed)
tf.random.set_seed(seed)

def load_and_preprocess_data(csv_path):
	"""
	Carga y preprocesa los datos del CSV
	"""
	print("Cargando datos...")
	df = pd.read_csv(csv_path)
	
	# Mostrar información básica
	print(f"Forma del dataset: {df.shape}")
	print(f"\nValores nulos por columna:\n{df.isnull().sum()}")
	
	# Eliminar duplicados si existen
	df_original_size = len(df)
	df = df.drop_duplicates()
	print(f"\nDuplicados eliminados: {df_original_size - len(df)}")
	
	# Separar features y target
	X = df.drop('liver_cancer', axis=1)
	y = df['liver_cancer']
	
	# Codificar variables categóricas
	categorical_columns = ['gender', 'alcohol_consumption', 'smoking_status', 'physical_activity_level']
	
	# Crear diccionario para guardar los encoders
	encoders = {}
	
	for col in categorical_columns:
		le = LabelEncoder()
		X[col] = le.fit_transform(X[col])
		encoders[col] = le
	
	# Guardar los nombres de las features
	feature_names = X.columns.tolist()
	
	return X, y, feature_names, encoders

def build_model(hp, input_dim):
	"""
	Construye el modelo con hiperparámetros tunables usando Keras Tuner
	
	Args:
		hp: Objeto HyperParameters de Keras Tuner
		input_dim: Dimensión de entrada (número de features)
	
	Returns:
		Modelo compilado
	"""
	model = Sequential()
	
	# Capa de entrada con hiperparámetros tunables
	model.add(Dense(
		units=hp.Int('units_layer_1', min_value=32, max_value=256, step=32),
		activation=hp.Choice('activation_layer_1', values=['relu', 'tanh']),
		input_shape=(input_dim,)
	))
	model.add(Dropout(hp.Float('dropout_1', min_value=0.1, max_value=0.5, step=0.1)))
	
	# Número de capas ocultas adicionales (1-3)
	num_layers = hp.Int('num_layers', min_value=1, max_value=3)
	
	for i in range(num_layers):
		model.add(Dense(
			units=hp.Int(f'units_layer_{i+2}', min_value=16, max_value=128, step=16),
			activation=hp.Choice(f'activation_layer_{i+2}', values=['relu', 'tanh'])
		))
		model.add(Dropout(hp.Float(f'dropout_{i+2}', min_value=0.1, max_value=0.4, step=0.1)))
	
	# Capa de salida
	model.add(Dense(1, activation='sigmoid'))
	
	# Optimizador tunable
	learning_rate = hp.Float('learning_rate', min_value=1e-4, max_value=1e-2, sampling='log')
	opt = tf.keras.optimizers.Adam(learning_rate=learning_rate)
	
	# Compilar modelo
	model.compile(
		optimizer=opt,
		loss='binary_crossentropy',
		metrics=['accuracy', tf.keras.metrics.AUC(name='auc')]
	)
	
	return model

def plot_training_history(history):
	"""
	Visualiza el historial de entrenamiento
	"""
	fig, axes = plt.subplots(1, 3, figsize=(15, 5))
	
	# Loss
	axes[0].plot(history.history['loss'], label='Train')
	axes[0].plot(history.history['val_loss'], label='Validation')
	axes[0].set_title('Model Loss')
	axes[0].set_xlabel('Epoch')
	axes[0].set_ylabel('Loss')
	axes[0].legend()
	
	# Accuracy
	axes[1].plot(history.history['accuracy'], label='Train')
	axes[1].plot(history.history['val_accuracy'], label='Validation')
	axes[1].set_title('Model Accuracy')
	axes[1].set_xlabel('Epoch')
	axes[1].set_ylabel('Accuracy')
	axes[1].legend()
	
	# AUC
	axes[2].plot(history.history['auc'], label='Train')
	axes[2].plot(history.history['val_auc'], label='Validation')
	axes[2].set_title('Model AUC')
	axes[2].set_xlabel('Epoch')
	axes[2].set_ylabel('AUC')
	axes[2].legend()
	
	plt.tight_layout()
	plt.savefig('model/training_history.png')
	plt.close()

def evaluate_model(model, X_test, y_test, scaler):
	"""
	Evalúa el modelo y genera métricas
	"""
	# Escalar datos de prueba
	X_test_scaled = scaler.transform(X_test)
	
	# Predicciones
	y_pred_proba = model.predict(X_test_scaled)
	y_pred = (y_pred_proba > 0.5).astype(int)
	
	# Métricas
	print("\n=== Evaluación del Modelo ===")
	print("\nReporte de Clasificación:")
	print(classification_report(y_test, y_pred, target_names=['No Cáncer', 'Cáncer']))
	
	# Matriz de confusión
	cm = confusion_matrix(y_test, y_pred)
	plt.figure(figsize=(8, 6))
	sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
				xticklabels=['No Cáncer', 'Cáncer'],
				yticklabels=['No Cáncer', 'Cáncer'])
	plt.title('Matriz de Confusión')
	plt.ylabel('Etiqueta Real')
	plt.xlabel('Predicción')
	plt.savefig('model/confusion_matrix.png')
	plt.close()
	
	# ROC Curve
	auc_score = roc_auc_score(y_test, y_pred_proba)
	fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
	
	plt.figure(figsize=(8, 6))
	plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {auc_score:.3f})')
	plt.plot([0, 1], [0, 1], 'k--', label='Random')
	plt.xlabel('False Positive Rate')
	plt.ylabel('True Positive Rate')
	plt.title('ROC Curve')
	plt.legend()
	plt.savefig('model/roc_curve.png')
	plt.close()
	
	print(f"\nAUC Score: {auc_score:.4f}")
	
	# Evaluación final del modelo
	test_loss, test_accuracy, test_auc = model.evaluate(X_test_scaled, y_test, verbose=0)
	print(f"\nTest Loss: {test_loss:.4f}")
	print(f"Test Accuracy: {test_accuracy:.4f}")
	print(f"Test AUC: {test_auc:.4f}")

def run_hyperparameter_search(X_train_scaled, y_train, input_dim, tuner_dir):
	"""
	Ejecuta la búsqueda de hiperparámetros usando Keras Tuner
	
	Args:
		X_train_scaled: Datos de entrenamiento escalados
		y_train: Etiquetas de entrenamiento
		input_dim: Dimensión de entrada
		tuner_dir: Directorio para guardar resultados del tuner
	
	Returns:
		best_hps: Mejores hiperparámetros encontrados
		tuner: Objeto tuner
	"""
	print("\n" + "="*60)
	print("INICIANDO BÚSQUEDA DE HIPERPARÁMETROS CON KERAS TUNER")
	print("="*60)
	
	# Definir el tuner usando Hyperband
	tuner = kt.Hyperband(
		lambda hp: build_model(hp, input_dim),
		objective=kt.Objective('val_auc', direction='max'),
		max_epochs=50,
		factor=3,
		seed=seed,
		directory=tuner_dir,
		project_name='liver_cancer_tuning',
		overwrite=True
	)
	
	# Mostrar espacio de búsqueda
	print("\nEspacio de búsqueda de hiperparámetros:")
	print("- Unidades capa 1: 32-256 (step 32)")
	print("- Número de capas ocultas: 1-3")
	print("- Unidades capas ocultas: 16-128 (step 16)")
	print("- Activación: relu, tanh")
	print("- Dropout: 0.1-0.5")
	print("- Learning rate: 1e-4 a 1e-2 (log scale)")
	print("- Optimizador: adam, rmsprop")
	
	# Callback para early stopping durante el tuning
	early_stopping = EarlyStopping(
		monitor='val_auc',
		mode='max',
		patience=5,
		restore_best_weights=True,
		verbose=0
	)
	
	# Ejecutar búsqueda
	print("\nBuscando mejores hiperparámetros...")
	tuner.search(
		X_train_scaled, y_train,
		validation_split=0.2,
		epochs=50,
		batch_size=32,
		callbacks=[early_stopping],
		verbose=1
	)
	
	# Obtener mejores hiperparámetros
	best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]
	
	print("\n" + "="*60)
	print("MEJORES HIPERPARÁMETROS ENCONTRADOS")
	print("="*60)
	print(f"Unidades capa 1: {best_hps.get('units_layer_1')}")
	print(f"Activación capa 1: {best_hps.get('activation_layer_1')}")
	print(f"Dropout 1: {best_hps.get('dropout_1')}")
	print(f"Número de capas ocultas: {best_hps.get('num_layers')}")
	
	for i in range(best_hps.get('num_layers')):
		print(f"Unidades capa {i+2}: {best_hps.get(f'units_layer_{i+2}')}")
		print(f"Activación capa {i+2}: {best_hps.get(f'activation_layer_{i+2}')}")
		print(f"Dropout {i+2}: {best_hps.get(f'dropout_{i+2}')}")
	
	print(f"Learning rate: {best_hps.get('learning_rate')}")
	print("="*60)
	
	return best_hps, tuner

def main():
	"""
	Función principal de entrenamiento con Keras Tuner
	"""
	# Configuración
	DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'liver_cancer_data_clean.csv')
	MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'backend', 'saved_models')
	TUNER_DIR = os.path.join(os.path.dirname(__file__), 'tuner_results')
	
	# Crear directorios si no existen
	os.makedirs(MODEL_DIR, exist_ok=True)
	os.makedirs('model', exist_ok=True)
	os.makedirs(TUNER_DIR, exist_ok=True)
	
	# 1. Cargar y preprocesar datos
	print("="*60)
	print("FASE 1: CARGA Y PREPROCESAMIENTO DE DATOS")
	print("="*60)
	X, y, feature_names, encoders = load_and_preprocess_data(DATA_PATH)
	
	# 2. División train/test
	X_train, X_test, y_train, y_test = train_test_split(
		X, y, test_size=0.2, random_state=seed, stratify=y
	)
	
	print(f"\nTamaño del conjunto de entrenamiento: {X_train.shape}")
	print(f"Tamaño del conjunto de prueba: {X_test.shape}")
	print(f"Distribución de clases (train): {np.bincount(y_train)}")
	print(f"Distribución de clases (test): {np.bincount(y_test)}")
	
	# 3. Escalado de características
	print("\n" + "="*60)
	print("FASE 2: ESCALADO DE CARACTERÍSTICAS")
	print("="*60)
	scaler = StandardScaler()
	X_train_scaled = scaler.fit_transform(X_train)
	X_test_scaled = scaler.transform(X_test)
	print("Escalado completado con StandardScaler")
	
	# 4. Búsqueda de hiperparámetros con Keras Tuner
	input_dim = X_train_scaled.shape[1]
	best_hps, tuner = run_hyperparameter_search(X_train_scaled, y_train, input_dim, TUNER_DIR)
	
	# 5. Construir y entrenar el mejor modelo
	print("\n" + "="*60)
	print("FASE 3: ENTRENAMIENTO DEL MEJOR MODELO")
	print("="*60)
	
	# Construir modelo con mejores hiperparámetros
	best_model = tuner.hypermodel.build(best_hps)
	print("\nArquitectura del mejor modelo:")
	best_model.summary()
	
	# Callbacks para entrenamiento final
	early_stopping = EarlyStopping(
		monitor='val_auc',
		mode='max',
		patience=15,
		restore_best_weights=True,
		verbose=1
	)
	
	model_checkpoint = ModelCheckpoint(
		os.path.join(MODEL_DIR, 'best_model.h5'),
		monitor='val_auc',
		mode='max',
		save_best_only=True,
		verbose=1
	)
	
	# Entrenar modelo final con mejores hiperparámetros
	print("\nEntrenando modelo final con mejores hiperparámetros...")
	history = best_model.fit(
		X_train_scaled, y_train,
		validation_split=0.2,
		epochs=100,
		batch_size=32,
		callbacks=[early_stopping, model_checkpoint],
		verbose=1
	)
	
	# 6. Visualizar historial de entrenamiento
	print("\n" + "="*60)
	print("FASE 4: VISUALIZACIÓN Y EVALUACIÓN")
	print("="*60)
	plot_training_history(history)
	print("Gráficas de entrenamiento guardadas en: model/training_history.png")
	
	# 7. Evaluar modelo
	evaluate_model(best_model, X_test, y_test, scaler)
	
	# 8. Guardar artefactos
	print("\n" + "="*60)
	print("FASE 5: GUARDADO DE ARTEFACTOS")
	print("="*60)
	
	# Guardar modelo final
	best_model.save(os.path.join(MODEL_DIR, 'liver_cancer_model.h5'))
	print(f"Modelo guardado en: {MODEL_DIR}/liver_cancer_model.h5")
	
	# Guardar scaler
	with open(os.path.join(MODEL_DIR, 'scaler.pkl'), 'wb') as f:
		pickle.dump(scaler, f)
	print(f"Scaler guardado en: {MODEL_DIR}/scaler.pkl")
	
	# Guardar mejores hiperparámetros
	best_hyperparameters = {
		'units_layer_1': best_hps.get('units_layer_1'),
		'activation_layer_1': best_hps.get('activation_layer_1'),
		'dropout_1': best_hps.get('dropout_1'),
		'num_layers': best_hps.get('num_layers'),
		'learning_rate': best_hps.get('learning_rate')
	}
	
	# Agregar hiperparámetros de capas adicionales
	for i in range(best_hps.get('num_layers')):
		best_hyperparameters[f'units_layer_{i+2}'] = best_hps.get(f'units_layer_{i+2}')
		best_hyperparameters[f'activation_layer_{i+2}'] = best_hps.get(f'activation_layer_{i+2}')
		best_hyperparameters[f'dropout_{i+2}'] = best_hps.get(f'dropout_{i+2}')
	
	with open(os.path.join(MODEL_DIR, 'best_hyperparameters.json'), 'w') as f:
		json.dump(best_hyperparameters, f, indent=2)
	print(f"Mejores hiperparámetros guardados en: {MODEL_DIR}/best_hyperparameters.json")
	
	# Guardar metadata completa
	test_metrics = best_model.evaluate(X_test_scaled, y_test, verbose=0)
	metadata = {
		'feature_names': feature_names,
		'encoders': {col: encoder.classes_.tolist() for col, encoder in encoders.items()},
		'model_performance': {
			'test_loss': float(test_metrics[0]),
			'test_accuracy': float(test_metrics[1]),
			'test_auc': float(test_metrics[2])
		},
		'best_hyperparameters': best_hyperparameters,
		'tuning_method': 'Hyperband',
		'input_dim': input_dim
	}
	
	with open(os.path.join(MODEL_DIR, 'feature_metadata.json'), 'w') as f:
		json.dump(metadata, f, indent=2)
	print(f"Metadata completa guardada en: {MODEL_DIR}/feature_metadata.json")
	
	print("\n" + "="*60)
	print("¡ENTRENAMIENTO COMPLETADO EXITOSAMENTE!")
	print("="*60)
	print("\nResumen de resultados:")
	print(f"  • Test Accuracy: {metadata['model_performance']['test_accuracy']:.4f}")
	print(f"  • Test AUC: {metadata['model_performance']['test_auc']:.4f}")
	print(f"  • Arquitectura: {best_hps.get('num_layers')+1} capas ocultas")
	print("="*60)

if __name__ == "__main__":
	main()
