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

# Agrupar por barrio o distrito
def analyze_districts(df):
    district_group = df.groupby('neighbourhood_group_cleansed')['price'].mean().sort_values()
    return district_group

# Análisis de distritos en Madrid y Barcelona
madrid_district_prices = analyze_districts(madrid_filtered)
barcelona_district_prices = analyze_districts(barcelona_filtered)

# Función para añadir los valores dentro de las barras
def add_value_labels(ax):
    for p in ax.patches:
        _x = p.get_x() + p.get_width() / 2
        _y = p.get_y() + p.get_height() / 2
        value = '{:.1f}'.format(p.get_width())
        ax.text(_x, _y, value, ha="center", va="center", color="black")

# Visualizar los precios medianos por distrito en un gráfico de barras
plt.figure(figsize=(12, 8))

# Gráfico para Madrid
plt.subplot(1, 2, 1)
ax1 = sns.barplot(x=madrid_district_prices.values, y=madrid_district_prices.index, palette='Blues', hue=madrid_district_prices.index, dodge=False)
plt.title('Precio Medio por Distrito en Madrid')
plt.xlabel('Precio (EUR)')
plt.ylabel('')
add_value_labels(ax1)

# Gráfico para Barcelona
plt.subplot(1, 2, 2)
ax2 = sns.barplot(x=barcelona_district_prices.values, y=barcelona_district_prices.index, palette='Oranges', hue=barcelona_district_prices.index, dodge=False)
plt.title('Precio Medio por Distrito en Barcelona')
plt.xlabel('Precio (EUR)')
plt.ylabel('')
add_value_labels(ax2)

plt.tight_layout()
plt.savefig('precios_por_distrito.png')
plt.show()

# Gráfico para la cantidad de alojamientos en los 3 distritos más económicos y 3 más caros
def plot_accommodation_counts(city_data, district_prices, city_name):
    cheapest_districts = district_prices.nsmallest(3)
    most_expensive_districts = district_prices.nlargest(3)
    
    # Contar la cantidad de alojamientos en los distritos
    cheapest_count = city_data[city_data['neighbourhood_group_cleansed'].isin(cheapest_districts.index)].groupby('neighbourhood_group_cleansed').size()
    most_expensive_count = city_data[city_data['neighbourhood_group_cleansed'].isin(most_expensive_districts.index)].groupby('neighbourhood_group_cleansed').size()
    
    # Crear un nuevo DataFrame para los gráficos
    accommodation_counts = pd.DataFrame({
        'Distrito': cheapest_count.index.tolist() + most_expensive_count.index.tolist(),
        'Cantidad': cheapest_count.tolist() + most_expensive_count.tolist(),
        'Tipo': ['Económico'] * 3 + ['Caro'] * 3
    })
    
    plt.figure(figsize=(5, 6))
    if (city_name == 'Madrid'):
        sns.barplot(data=accommodation_counts, x='Distrito', y='Cantidad', hue='Tipo', palette='Blues')
    else:
        sns.barplot(data=accommodation_counts, x='Distrito', y='Cantidad', hue='Tipo', palette='Oranges')
    plt.title(f'Cantidad de Alojamientos en Distritos de {city_name}')
    plt.xlabel('Distrito')
    plt.ylabel('Cantidad de Alojamientos')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'cantidad_alojamientos_{city_name}.png')
    plt.show()

# Gráficos de cantidad de alojamientos en Madrid y Barcelona
plot_accommodation_counts(madrid_filtered, madrid_district_prices, "Madrid")
plot_accommodation_counts(barcelona_filtered, barcelona_district_prices, "Barcelona")