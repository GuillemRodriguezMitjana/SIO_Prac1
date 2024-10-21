# Importamos las bibliotecas necesarias
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Función que genera un boxplot para mostrar la valoración calidad-precio por distrito
def generar_boxplot_valoracion(archivo_csv, nombre_ciudad):
    # Cargamos los datos del CSV en un DataFrame
    datos = pd.read_csv(archivo_csv)
    # Filtramos las columnas relevantes para el análisis
    datos_filtrados = datos[['neighbourhood_group_cleansed', 'review_scores_value']]
    
    # Creamos el boxplot utilizando seaborn
    plt.figure(figsize=(12, 6))
    sns.boxplot(
        data=datos_filtrados, 
        x='neighbourhood_group_cleansed', 
        y='review_scores_value', 
        palette='muted'
    )
    # Ajustamos el título y las etiquetas de los ejes
    plt.title(f'Valoración Calidad-Precio por Distrito - {nombre_ciudad}', fontsize=14)
    plt.xlabel('Distrito', fontsize=12)
    plt.ylabel('Valoración Calidad-Precio', fontsize=12)
    # Rotamos las etiquetas del eje X para mejorar la legibilidad
    plt.xticks(rotation=45, fontsize=8)
    # Guardamos el gráfico con el nombre de la ciudad
    plt.savefig(f'boxplot_valoracion_{nombre_ciudad}.png')
    # Mostramos el gráfico
    plt.show()

# Definimos las rutas de los archivos CSV para Madrid y Barcelona
madrid_data = '../listings_madrid.csv'
barcelona_data = '../listings_barcelona.csv'

# Generamos los boxplots para Madrid y Barcelona
generar_boxplot_valoracion(madrid_data, 'Madrid')
generar_boxplot_valoracion(barcelona_data, 'Barcelona')