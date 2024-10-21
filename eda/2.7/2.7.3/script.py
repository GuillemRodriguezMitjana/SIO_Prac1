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

# Filtrar las variables de interés
madrid_data_filtered = madrid_data[['number_of_reviews', 'review_scores_rating', 'host_has_profile_pic']].dropna()
barcelona_data_filtered = barcelona_data[['number_of_reviews', 'review_scores_rating', 'host_has_profile_pic']].dropna()

# Convertir 'host_has_profile_pic' de "t"/"f" a "Sí"/"No" como strings
madrid_data_filtered['host_has_profile_pic'] = madrid_data_filtered['host_has_profile_pic'].replace({'t': 'Sí', 'f': 'No'})
barcelona_data_filtered['host_has_profile_pic'] = barcelona_data_filtered['host_has_profile_pic'].replace({'t': 'Sí', 'f': 'No'})

# Crear scatterplot para Madrid
plt.figure(figsize=(8, 4))
sns.scatterplot(x='review_scores_rating', y='number_of_reviews', hue='host_has_profile_pic', data=madrid_data_filtered, alpha=1, palette={'Sí': 'green', 'No': 'red'})
plt.title('Relación entre Puntuación y Número de Reseñas en Madrid')
plt.xlabel('Puntuación de Reseñas')
plt.ylabel('Número de Reseñas')
plt.legend(title='Foto de Perfil')
plt.savefig('puntuacion_numReseñas_Madrid.png')
plt.show()

# Crear scatterplot para Barcelona
plt.figure(figsize=(8, 4))
sns.scatterplot(x='review_scores_rating', y='number_of_reviews', hue='host_has_profile_pic', data=barcelona_data_filtered, alpha=1, palette={'Sí': 'green', 'No': 'red'})
plt.title('Relación entre Puntuación y Número de Reseñas en Barcelona')
plt.xlabel('Puntuación de Reseñas')
plt.ylabel('Número de Reseñas')
plt.legend(title='Foto de Perfil')
plt.savefig('puntuacion_numReseñas_Barcelona.png')
plt.show()
