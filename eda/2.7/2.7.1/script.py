import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar los datos
madrid_data = pd.read_csv('../../listings_madrid.csv')
barcelona_data = pd.read_csv('../../listings_barcelona.csv')

# Limpiar la columna de precios
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
    df = df[(df['price'] >= lower_bound) & (df['price'] <= upper_bound)]
    return df

# Eliminar outliers en ambos datasets
madrid_data = remove_outliers(madrid_data)
barcelona_data = remove_outliers(barcelona_data)

# Filtrar solo las variables seleccionadas
madrid_data_filtered = madrid_data[['price', 'number_of_reviews', 'host_identity_verified']].dropna()
barcelona_data_filtered = barcelona_data[['price', 'number_of_reviews', 'host_identity_verified']].dropna()

# Convertir 'host_identity_verified' de 't'/'f' a 'Sí'/'No'
madrid_data_filtered['host_identity_verified'] = madrid_data_filtered['host_identity_verified'].replace({'t': 'Sí', 'f': 'No'})
barcelona_data_filtered['host_identity_verified'] = barcelona_data_filtered['host_identity_verified'].replace({'t': 'Sí', 'f': 'No'})

# Crear el scatter plot para Madrid
plt.figure(figsize=(10, 6))
sns.scatterplot(data=madrid_data_filtered, x='price', y='number_of_reviews', hue='host_identity_verified', palette={'Sí': 'green', 'No': 'red'})
plt.title('Relación entre Precio y Número de Reseñas en Madrid')
plt.xlabel('Precio')
plt.ylabel('Número de Reseñas')
plt.legend(title='Host Verificado')
plt.tight_layout()
plt.savefig('precio_numReviews_Madrid.png')
plt.show()

# Crear el scatter plot para Barcelona
plt.figure(figsize=(10, 6))
sns.scatterplot(data=barcelona_data_filtered, x='price', y='number_of_reviews', hue='host_identity_verified', palette={'Sí': 'green', 'No': 'red'})
plt.title('Relación entre Precio y Número de Reseñas en Barcelona')
plt.xlabel('Precio')
plt.ylabel('Número de Reseñas')
plt.legend(title='Host Verificado')
plt.tight_layout()
plt.savefig('precio_numReviews_Barcelona.png')
plt.show()
