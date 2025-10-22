"""
Script de entrenamiento para el modelo de predicción de cáncer de hígado
Entrena una Red Neuronal Multicapa (MLP) usando TensorFlow/Keras
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
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar semilla para reproducibilidad
np.random.seed(42)
tf.random.set_seed(42)

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

def create_model(input_dim):
    """
    Crea el modelo de Red Neuronal Multicapa
    """
    model = Sequential([
        # Capa de entrada
        Dense(64, activation='relu', input_shape=(input_dim,)),
        Dropout(0.3),
        
        # Capa oculta
        Dense(32, activation='relu'),
        Dropout(0.2),
        
        # Capa de salida con sigmoid para probabilidad
        Dense(1, activation='sigmoid')
    ])
    
    # Compilar el modelo
    model.compile(
        optimizer='adam',
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

def main():
    """
    Función principal de entrenamiento
    """
    # Configuración
    DATA_PATH = '../data/liver_cancer_data.csv'
    MODEL_DIR = '../backend/saved_models'
    
    # Crear directorio para modelos si no existe
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs('model', exist_ok=True)
    
    # 1. Cargar y preprocesar datos
    X, y, feature_names, encoders = load_and_preprocess_data(DATA_PATH)
    
    # 2. División train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nTamaño del conjunto de entrenamiento: {X_train.shape}")
    print(f"Tamaño del conjunto de prueba: {X_test.shape}")
    
    # 3. Escalado de características
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 4. Crear modelo
    model = create_model(X_train_scaled.shape[1])
    model.summary()
    
    # 5. Callbacks
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=10,
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
    
    # 6. Entrenar modelo
    print("\nEntrenando modelo...")
    history = model.fit(
        X_train_scaled, y_train,
        validation_split=0.2,
        epochs=50,
        batch_size=32,
        callbacks=[early_stopping, model_checkpoint],
        verbose=1
    )
    
    # 7. Visualizar historial de entrenamiento
    plot_training_history(history)
    
    # 8. Evaluar modelo
    evaluate_model(model, X_test, y_test, scaler)
    
    # 9. Guardar artefactos
    # Guardar modelo final
    model.save(os.path.join(MODEL_DIR, 'liver_cancer_model.h5'))
    print(f"\nModelo guardado en: {MODEL_DIR}/liver_cancer_model.h5")
    
    # Guardar scaler
    with open(os.path.join(MODEL_DIR, 'scaler.pkl'), 'wb') as f:
        pickle.dump(scaler, f)
    print(f"Scaler guardado en: {MODEL_DIR}/scaler.pkl")
    
    # Guardar metadata
    metadata = {
        'feature_names': feature_names,
        'encoders': {col: encoder.classes_.tolist() for col, encoder in encoders.items()},
        'model_performance': {
            'test_accuracy': float(model.evaluate(X_test_scaled, y_test, verbose=0)[1]),
            'test_auc': float(model.evaluate(X_test_scaled, y_test, verbose=0)[2])
        }
    }
    
    with open(os.path.join(MODEL_DIR, 'feature_metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"Metadata guardada en: {MODEL_DIR}/feature_metadata.json")
    
    print("\n¡Entrenamiento completado exitosamente!")

if __name__ == "__main__":
    main()
