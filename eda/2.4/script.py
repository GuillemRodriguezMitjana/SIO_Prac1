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

# Filtrar solo los alojamientos que están disponibles
madrid_data = madrid_data[madrid_data['has_availability'] == 't']
barcelona_data = barcelona_data[barcelona_data['has_availability'] == 't']

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

# Función para añadir los valores en las barras
def add_value_labels(ax):
    for p in ax.patches:
        if p.get_height() == 0: return
        ax.annotate(format(p.get_height(), '.0f'),
                    (p.get_x() + p.get_width() / 2, p.get_height()),
                    ha="center", va="bottom", color="black")

# Cantidad total de alojamientos disponibles en cada ciudad
total_madrid = madrid_filtered.shape[0]
total_barcelona = barcelona_filtered.shape[0]

# Crear un DataFrame para visualizar la comparación total de disponibilidad
availability_comparison = pd.DataFrame({
    'Ciudad': ['Madrid', 'Barcelona'],
    'Cantidad de Alojamientos': [total_madrid, total_barcelona]
})

# Gráfico de barras comparando la cantidad total de alojamientos
plt.figure(figsize=(6, 4))
ax = sns.barplot(data=availability_comparison, x='Ciudad', y='Cantidad de Alojamientos', palette='muted', hue='Ciudad', legend=False)
add_value_labels(ax)
plt.title('Comparación de Disponibilidad de Alojamientos')
plt.ylabel('Cantidad de Alojamientos')
plt.ylim(0, 22000)
plt.tight_layout()
plt.savefig('disponibilidad_total_alojamientos.png')
plt.show()

# Definir los rangos de precios en función del salario mensual medio
# Sueldo medio neto -> 1800 / 30 dias = 60 EUR/dia
# Sabiendo eso consideramos que:
#   - El sueldo de un dia es un precio barato
#   - El sueldo de hasta dos dias es un precio normal
#   - El sueldo de más de dos dias es un precio caro
def categorize_price(price):
    if price <= 60:
        return 'Económico'
    elif 60 < price <= 120:
        return 'Normal'
    else:
        return 'Caro'

# Aplicar la categorización a los datasets
madrid_filtered['Rango Precio'] = madrid_filtered['price'].apply(categorize_price)
barcelona_filtered['Rango Precio'] = barcelona_filtered['price'].apply(categorize_price)

# Contar cuántos alojamientos hay en cada rango de precios para cada ciudad
madrid_price_counts = madrid_filtered['Rango Precio'].value_counts().reindex(['Económico', 'Normal', 'Caro'])
barcelona_price_counts = barcelona_filtered['Rango Precio'].value_counts().reindex(['Económico', 'Normal', 'Caro'])

# Crear un DataFrame para visualizar los resultados
price_comparison = pd.DataFrame({
    'Ciudad': ['Madrid'] * 3 + ['Barcelona'] * 3,
    'Rango Precio': ['Económico\n(0-60€)', 'Normal\n(61-120€)', 'Caro\n(>120€)'] * 2,
    'Cantidad de Alojamientos': madrid_price_counts.tolist() + barcelona_price_counts.tolist()
})

# Gráfico de barras comparando los rangos de precios entre ambas ciudades
plt.figure(figsize=(8, 6))
ax = sns.barplot(data=price_comparison, x='Rango Precio', y='Cantidad de Alojamientos', hue='Ciudad', palette='muted')
add_value_labels(ax)
plt.title('Comparación de Alojamientos por Rango de Precios en Madrid y Barcelona')
plt.ylabel('Cantidad de Alojamientos')
plt.ylim(0, 11000)
plt.tight_layout()
plt.savefig('comparacion_alojamientos_por_precios.png')
plt.show()
