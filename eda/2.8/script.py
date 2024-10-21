import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
from collections import Counter

# Cargar los datos
madrid_data = pd.read_csv('../listings_madrid.csv')
barcelona_data = pd.read_csv('../listings_barcelona.csv')

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

# Convertir la columna 'amenities' de JSON a lista
def parse_amenities(amenities_str):
    try:
        return json.loads(amenities_str)
    except json.JSONDecodeError:
        return []

# Aplicar la conversión a cada fila de la columna 'amenities' para ambos datasets
madrid_data['amenities_list'] = madrid_data['amenities'].apply(parse_amenities)
barcelona_data['amenities_list'] = barcelona_data['amenities'].apply(parse_amenities)

# Contar la frecuencia de servicios
madrid_services = [service for amenities in madrid_data['amenities_list'] for service in amenities]
madrid_service_counts = Counter(madrid_services)
barcelona_services = [service for amenities in barcelona_data['amenities_list'] for service in amenities]
barcelona_service_counts = Counter(barcelona_services)

# Función para crear gráfico de pastel
def plot_pie_chart(service_counts, city_name):
    # Obtener los 15 servicios más comunes
    top_services = service_counts.most_common(15)
    
    # Separar los servicios y sus frecuencias
    services, counts = zip(*top_services)
    
    # Sumar la frecuencia de los demás servicios para la categoría 'Otros'
    other_count = sum(count for service, count in service_counts.items() if service not in services)
    
    # Añadir la categoría 'Otros'
    if other_count > 0:
        services += ('Otros',)
        counts += (other_count,)
    
    # Crear el gráfico de pastel
    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=services, autopct='%1.1f%%', startangle=90)
    plt.title(f'Proporción de Servicios en {city_name}')
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(f'servicios_{city_name}.png')
    plt.show()

# Crear gráficos de pastel para ambas ciudades
plot_pie_chart(madrid_service_counts, 'Madrid')
plot_pie_chart(barcelona_service_counts, 'Barcelona')

# Contar el número de servicios
madrid_data['num_services'] = madrid_data['amenities_list'].apply(len)
barcelona_data['num_services'] = barcelona_data['amenities_list'].apply(len)

# Especificar la paleta de colores
palette = {'Entire home/apt': '#1f77b4', 'Private room': '#ff7f0e', 'Shared room': '#2ca02c', 'Hotel room': '#d62728'}

# Crear las variables para el eje X
def categorize_services(num):
    if num > 50:
        return '+50'
    else:
        return str(num)

madrid_data['service_category'] = madrid_data['num_services'].apply(categorize_services)
barcelona_data['service_category'] = barcelona_data['num_services'].apply(categorize_services)

# Convertir 'service_category' a tipo categórico y definir el orden
category_order = [str(i) for i in range(0, 51)] + ['+50']
madrid_data['service_category'] = pd.Categorical(madrid_data['service_category'], categories=category_order, ordered=True)
barcelona_data['service_category'] = pd.Categorical(barcelona_data['service_category'], categories=category_order, ordered=True)

# Crear el scatterplot para Madrid
plt.figure(figsize=(12, 6))
sns.scatterplot(data=madrid_data, x='service_category', y='price', hue='room_type', palette=palette)
plt.title('Relación entre Número de Servicios y Precio en Madrid')
plt.xlabel('Número de Servicios')
plt.ylabel('Precio (EUR)')
plt.xticks(rotation=45)
plt.legend(title='Tipo de Habitación')
plt.tight_layout()
plt.savefig('precio_numServicios_Madrid.png')
plt.show()

# Crear el scatterplot para Barcelona
plt.figure(figsize=(12, 6))
sns.scatterplot(data=barcelona_data, x='service_category', y='price', hue='room_type', palette=palette)
plt.title('Relación entre Número de Servicios y Precio en Barcelona')
plt.xlabel('Número de Servicios')
plt.ylabel('Precio (EUR)')
plt.xticks(rotation=45)
plt.legend(title='Tipo de Habitación')
plt.tight_layout()
plt.savefig('precio_numServicios_Barcelona.png')
plt.show()

# Calcular coeficientes de correlación entre precio y número de servicios según el tipo de habitación
madrid_corr = madrid_data.groupby('room_type').apply(lambda x: x['price'].corr(x['num_services'])).reset_index(name='Coeficiente de Correlación').round(2)
barcelona_corr = barcelona_data.groupby('room_type').apply(lambda x: x['price'].corr(x['num_services'])).reset_index(name='Coeficiente de Correlación').round(2)

# Función para crear y guardar una tabla de correlación
def create_corr_table(corr_df, city_name):
    fig, ax = plt.subplots(figsize=(5, 2))
    ax.axis('tight')
    ax.axis('off')

    # Crear tabla
    table = ax.table(cellText=corr_df.values, 
                     colLabels=corr_df.columns, 
                     cellLoc='center', 
                     loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)

    # Aplicar negrita a la primera fila y columna
    for (i, j), cell in table.get_celld().items():
        if i == 0 or j == -1:
            cell.set_text_props(fontweight='bold')
    
    plt.title(city_name)
    plt.tight_layout()
    plt.savefig(f'tabla_correlacion_precio_numServicios_{city_name}.png')
    plt.show()

# Crear tablas de correlación
create_corr_table(madrid_corr, 'Madrid')
create_corr_table(barcelona_corr, 'Barcelona')