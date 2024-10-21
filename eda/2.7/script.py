import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar los datos
madrid_data = pd.read_csv('../listings_madrid.csv')
barcelona_data = pd.read_csv('../listings_barcelona.csv')

# Limpiar la columna de precios
def clean_price_column(df):
    df['price'] = df['price'].replace({'\$': '', ',': ''}, regex=True).astype(float)
    return df

madrid_data = clean_price_column(madrid_data)
barcelona_data = clean_price_column(barcelona_data)

# Filtrar solo las variables cuantitativas seleccionadas
variables_cuantitativas = ['price', 'number_of_reviews', 'review_scores_rating', 'accommodates']

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

# Eliminar filas con valores nulos en ambos datasets
madrid_data = madrid_data[variables_cuantitativas].dropna()
barcelona_data = barcelona_data[variables_cuantitativas].dropna()

# Función para crear y guardar una tabla de correlación
def create_corr_table(corr_matrix, city_name):
    fig, ax = plt.subplots(figsize=(9, 2))
    ax.axis('tight')
    ax.axis('off')

    # Crear la tabla
    table = ax.table(cellText=corr_matrix.values, 
                     rowLabels=corr_matrix.index, 
                     colLabels=corr_matrix.columns, 
                     cellLoc='center', 
                     loc='center')
    table.set_fontsize(10)
    table.scale(1.2, 1.2)

    # Poner en negrita la primera fila y columna
    for (i, j), cell in table.get_celld().items():
        if i == 0 or j == -1:
            cell.set_text_props(fontweight='bold')

    plt.tight_layout()
    plt.savefig(f'tabla_correlacion_{city_name}.png')

# Crear la tabla y la matriz de correlación para Madrid
create_corr_table(madrid_data.corr().round(2), "Madrid")
sns.pairplot(madrid_data, diag_kind=None)
plt.tight_layout()
plt.savefig('matriz_correlacion_Madrid.png')
plt.show()

# Crear la tabla y la matriz de correlación para Barcelona
create_corr_table(barcelona_data.corr().round(2), "Barcelona")
sns.pairplot(barcelona_data, diag_kind=None)
plt.tight_layout()
plt.savefig('matriz_correlacion_Barcelona.png')
plt.show()