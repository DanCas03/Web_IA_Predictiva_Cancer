"""
Script para convertir synthetic_liver_cancer_dataset.sql a CSV
Parsea los INSERT statements y extrae los datos a formato tabular
"""

import re
import pandas as pd
import os
from typing import List, Optional

def parse_sql_to_csv(sql_file_path: str, output_csv_path: str) -> pd.DataFrame:
	"""
	Convierte un archivo SQL con INSERT statements a un archivo CSV
	"""
	# Leer el archivo SQL
	with open(sql_file_path, 'r', encoding='utf-8') as file:
		sql_content: str = file.read()
	
	# Extraer nombres de columnas del CREATE TABLE
	create_table_pattern: str = r'CREATE TABLE mytable\((.*?)\);'
	create_match: Optional[re.Match[str]] = re.search(create_table_pattern, sql_content, re.DOTALL)
	
	if create_match:
		columns_text: str = create_match.group(1)
		# Extraer nombres de columnas
		column_names: List[str] = []
		for line in columns_text.strip().split('\n'):
			line: str = line.strip()
			if line and not line.startswith(')'):
				# Extraer el nombre de la columna (primera palabra, sin coma al inicio o final)
				col_name: str = line.split()[0].strip().lstrip(',').rstrip(',')
				column_names.append(col_name)
	
	# Parsear los INSERT statements
	insert_pattern = r'INSERT INTO mytable\([^)]+\) VALUES \(([^)]+)\);'
	insert_matches: List[str] = re.findall(insert_pattern, sql_content)
	
	# Procesar los datos
	data: List[List[str]] = []
	for match in insert_matches:
		# Dividir los valores y limpiarlos
		values: List[str] = []
		# Usar regex para manejar valores con comas dentro de strings
		value_pattern: str = r"'[^']*'|[^,]+"
		raw_values: List[str] = re.findall(value_pattern, match)
		
		for val in raw_values:
			val: str = val.strip()
			# Remover comillas simples si es string
			if val.startswith("'") and val.endswith("'"):
				val = val[1:-1]
			values.append(val)
		
		data.append(values)
	
	# Crear DataFrame
	df: pd.DataFrame = pd.DataFrame(data, columns=column_names)
	
	# Convertir tipos de datos apropiados
	# Columnas numéricas
	numeric_columns: List[str] = ['age', 'bmi', 'liver_function_score', 'alpha_fetoprotein_level']
	for col in numeric_columns:
		if col in df.columns:
			df[col] = pd.to_numeric(df[col], errors='coerce')
	
	# Columnas binarias (BIT)
	binary_columns: List[str] = ['hepatitis_b', 'hepatitis_c', 'cirrhosis_history', 
					'family_history_cancer', 'diabetes', 'liver_cancer']
	for col in binary_columns:
		if col in df.columns:
			df[col] = df[col].astype(int)
	
	# Crear directorio data si no existe
	os.makedirs('data', exist_ok=True)
	
	# Guardar como CSV
	df.to_csv(output_csv_path, index=False)
	
	# Mostrar información sobre el dataset
	print(f"Dataset exportado exitosamente a: {output_csv_path}")
	print(f"Forma del dataset: {df.shape}")
	print(f"Columnas: {list(df.columns)}")
	print("\nPrimeras 5 filas:")
	print(df.head())
	print("\nInformación del dataset:")
	print(df.info())
	print("\nDistribución de la variable objetivo (liver_cancer):")
	print(df['liver_cancer'].value_counts())
	
	return df

if __name__ == "__main__":
	# Rutas de archivos
	sql_file: str = "synthetic_liver_cancer_dataset.sql"
	csv_file: str = "data/liver_cancer_data.csv"
	
	# Ejecutar conversión
	df: pd.DataFrame = parse_sql_to_csv(sql_file, csv_file)

# ...existing code...

# Guardar df como pickle para uso en otro script
df.to_pickle('data/liver_cancer_data.pkl')

# en el indice 23 y el 8 habían errores en los datos, los cuales fueron corregidos manualmente en el archivo csv generado.