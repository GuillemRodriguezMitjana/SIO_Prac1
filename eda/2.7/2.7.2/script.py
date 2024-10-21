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
madrid_data_filtered = madrid_data[['price', 'accommodates', 'room_type']].dropna()
barcelona_data_filtered = barcelona_data[['price', 'accommodates', 'room_type']].dropna()

# Calcular coeficientes de correlación por tipo de habitación
madrid_corr = madrid_data_filtered.groupby('room_type').apply(lambda x: x['price'].corr(x['accommodates'])).round(2)
barcelona_corr = barcelona_data_filtered.groupby('room_type').apply(lambda x: x['price'].corr(x['accommodates'])).round(2)

# Función para crear y guardar una tabla de correlación
def create_corr_table(corr_series, city_name):
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.axis('tight')
    ax.axis('off')
    
    # Crear la tabla
    table = ax.table(cellText=corr_series.values.reshape(-1, 1), 
                     rowLabels=corr_series.index, 
                     colLabels=['Coeficiente de Correlación'], 
                     cellLoc='center', 
                     loc='center')
    
    table.set_fontsize(10)
    table.scale(1.2, 1.2)

    # Aplicar negrita a la primera fila y columna
    for (i, j), cell in table.get_celld().items():
        if i == 0 or j == -1:
            cell.set_text_props(fontweight='bold')

    plt.title(city_name);
    plt.tight_layout()
    plt.savefig(f'tabla_correlacion_precio_maxHuespedes_{city_name}.png')

# Crear tablas de correlación
create_corr_table(madrid_corr, "Madrid")
create_corr_table(barcelona_corr, "Barcelona")

# Especificar el orden de las categorías de room_type y sus colores asociados
room_type_order = ['Entire home/apt', 'Private room', 'Shared room', 'Hotel room']
palette = {'Entire home/apt': '#1f77b4', 'Private room': '#ff7f0e', 'Shared room': '#2ca02c', 'Hotel room': '#d62728'}

# Crear el scatter plot para Madrid
g = sns.FacetGrid(madrid_data_filtered, col='room_type', col_wrap=2, height=4, aspect=1.2, hue='room_type', palette=palette, col_order=room_type_order)
g.map(sns.scatterplot, 'accommodates', 'price')
g.set_titles(col_template="{col_name}")
g.set_axis_labels('Máximo de huéspedes', 'Precio')
plt.savefig('precio_maxHuespedes_Madrid.png')
plt.show()

# Crear el scatter plot para Barcelona
g = sns.FacetGrid(barcelona_data_filtered, col='room_type', col_wrap=2, height=4, aspect=1.2, hue='room_type', palette=palette, col_order=room_type_order)
g.map(sns.scatterplot, 'accommodates', 'price')
g.set_titles(col_template="{col_name}")
g.set_axis_labels('Máximo de huéspedes', 'Precio')
plt.savefig('precio_maxHuespedes_Barcelona.png')
plt.show()

# Obtener las frecuencias de room_type
madrid_room_type_counts = madrid_data_filtered['room_type'].value_counts()
barcelona_room_type_counts = barcelona_data_filtered['room_type'].value_counts()

# Definir un explode para destacar las categorías pequeñas
explode = [0.1 if val < 0.01 else 0 for val in madrid_room_type_counts / madrid_room_type_counts.sum()]
explode = [0.1 if val < 0.005 else 0 for val in barcelona_room_type_counts / barcelona_room_type_counts.sum()]

# Crear gráfico de tarta para Madrid
plt.figure(figsize=(6, 6))
plt.pie(madrid_room_type_counts, labels=madrid_room_type_counts.index, autopct='%1.1f%%', startangle=90, explode=explode, 
        colors=[palette[key] for key in madrid_room_type_counts.index], pctdistance=0.85)
plt.title('Proporción de Tipos de Habitaciones en Madrid')
plt.tight_layout()
plt.savefig('tipoHabitacion_Madrid.png')
plt.show()

# Crear gráfico de tarta para Barcelona
plt.figure(figsize=(6, 6))
plt.pie(barcelona_room_type_counts, labels=barcelona_room_type_counts.index, autopct='%1.1f%%', startangle=90, explode=explode, 
        colors=[palette[key] for key in barcelona_room_type_counts.index], pctdistance=0.85)
plt.title('Proporción de Tipos de Habitaciones en Barcelona')
plt.tight_layout()
plt.savefig('tipoHabitacion_Barcelona.png')
plt.show()