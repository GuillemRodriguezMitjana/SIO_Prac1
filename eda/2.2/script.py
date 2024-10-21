import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos de Madrid y Barcelona
madrid_data = pd.read_csv('../listings_madrid.csv')
barcelona_data = pd.read_csv('../listings_barcelona.csv')

# Convertir la columna de precios a numérica
def clean_price_column(df):
    df['price'] = df['price'].replace({'\$': '', ',': ''}, regex=True).astype(float)
    return df

madrid_data = clean_price_column(madrid_data)
barcelona_data = clean_price_column(barcelona_data)

# Función para eliminar outliers usando el rango intercuartílico (IQR)
def remove_outliers(df):
    Q1 = df['price'].quantile(0.25)
    Q3 = df['price'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df_filtered = df[(df['price'] >= lower_bound) & (df['price'] <= upper_bound)]
    return df_filtered

# Eliminar outliers en ambos datasets
madrid_filtered = remove_outliers(madrid_data)
barcelona_filtered = remove_outliers(barcelona_data)

# Calcular mediana, IQR y porcentaje de alojamientos por debajo de 200 EUR
def calculate_statistics(df, city_name):
    median = df['price'].median()
    Q1 = df['price'].quantile(0.25)
    Q3 = df['price'].quantile(0.75)
    IQR = Q3 - Q1
    below_200 = len(df[df['price'] < 200]) / len(df) * 100
    
    print(f"{city_name} - Mediana: {median} EUR, IQR: {IQR} EUR, % por debajo de 200 EUR: {below_200:.2f}%")

# Calcular estadísticas para Madrid y Barcelona
calculate_statistics(madrid_filtered, "Madrid")
calculate_statistics(barcelona_filtered, "Barcelona")

# Crear un histograma con precios en intervalos de 50 EUR
plt.figure(figsize=(10, 6))

# Histograma de Madrid con rangos de 50 EUR
sns.histplot(madrid_filtered['price'], bins=range(0, int(madrid_filtered['price'].max()) + 50, 50), 
             color='blue', kde=False, label='Madrid', alpha=0.5)

# Histograma de Barcelona con rangos de 50 EUR
sns.histplot(barcelona_filtered['price'], bins=range(0, int(barcelona_filtered['price'].max()) + 50, 50), 
             color='orange', kde=False, label='Barcelona', alpha=0.5)

# Añadir títulos y etiquetas
plt.title('Distribución de Precios en Madrid y Barcelona (Sin Outliers, Rango de 50 EUR)')
plt.xlabel('Precio (EUR)')
plt.ylabel('Frecuencia')
plt.legend()

# Guardar el gráfico de distribución de precios
plt.savefig('distribucion_precios.png')
plt.show()
