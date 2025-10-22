# %% [markdown]
# # Primero importo mi DataFrame

# %%
import pandas as pd
# Cargar df desde pickle
df = pd.read_pickle('data/liver_cancer_data.pkl')
# Ahora puedes usar df en este script
print("DataFrame cargado con éxito.")
print(df.head())

# %% [markdown]
# # Vamos a chequear si hay valores atípicos

# %%
import seaborn as sns
import matplotlib.pyplot as plt

for col in df.columns:
    plt.figure(figsize=(8, 6))
    sns.boxplot(x=df[col])
    plt.title(col)
    plt.show()