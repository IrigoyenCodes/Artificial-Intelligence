import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

#For further involvement in the code, change iris to 1,2, or 3.
df = pd.read_csv('iris.csv')
print(df.head())

# Verificar valores nulos
print(df.isnull().sum())


X = df.drop('species', axis=1)
y = df['species']


print(y.value_counts())

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled = pd.DataFrame(X_scaled, columns=X.columns)

print(X_scaled.head())

# Matriz de correlación
corr = X_scaled.corr()
plt.figure(figsize=(8,6))
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title('Matriz de Correlación')
plt.show() 
