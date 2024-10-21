# Biblioteca que facilita la manipulación de datos estructurados
import pandas as pd
# Biblioteca para crear gráficos y visualizaciones
import matplotlib.pyplot as plt

# Función que genera informe de propietarios con más alojamientos
def generar_informe_propietarios(archivo_csv, nombre_ciudad):
    # Leemos el CSV y lo cargamos en un DataFrame
    datos = pd.read_csv(archivo_csv)
    # Creamos una nueva columna que combine host_name y host_id
    datos['host_combined'] = datos['host_name'] + ' (' + datos['host_id'].astype(str) + ')'
    # Contamos cuántas veces aparece cada propietario y seleccionamos los 15 con más alojamientos
    frecuencia_top15 = datos['host_combined'].value_counts().head(15)
    # Convertimos la serie en un DataFrame y renombramos las columnas
    tabla_frecuencias = frecuencia_top15.reset_index()
    tabla_frecuencias.columns = ['Propietario', 'Frecuencia']
    # Calculamos la frecuencia relativa y el porcentaje
    tabla_frecuencias['Frecuencia relativa'] = tabla_frecuencias['Frecuencia'] / tabla_frecuencias['Frecuencia'].sum()
    tabla_frecuencias['Porcentaje'] = tabla_frecuencias['Frecuencia relativa'] * 100
    # Redondeamos los decimales
    tabla_frecuencias['Frecuencia relativa'] = tabla_frecuencias['Frecuencia relativa'].round(3)
    tabla_frecuencias['Porcentaje'] = tabla_frecuencias['Porcentaje'].round(2)
    # Crear y mostrar la tabla en un gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('tight')
    ax.axis('off')
    tabla = ax.table(cellText=tabla_frecuencias.values, colLabels=tabla_frecuencias.columns, cellLoc='center', loc='center')
    # Ponemos en negrita los encabezados
    for j in range(len(tabla_frecuencias.columns)):
        tabla[(0, j)].set_text_props(fontweight='bold')
    # Ajustamos el tamaño de las columnas automáticamente
    tabla.auto_set_column_width(range(len(tabla_frecuencias.columns)))
    # Mostramos la tabla
    plt.show()

    # Crear y mostrar la gráfica de barras
    plt.figure(figsize=(10, 6))
    plt.bar(tabla_frecuencias['Propietario'], tabla_frecuencias['Frecuencia'])
    plt.xticks(rotation=90)  # Rotamos las etiquetas para mayor claridad
    plt.title(f'Número de alojamientos por propietario - {nombre_ciudad}')
    plt.xlabel('Propietario (ID)')
    plt.ylabel('Número de alojamientos')
    plt.tight_layout()  # Ajusta el layout para que no se corten las etiquetas
    # Guardamos la gráfica con el nombre de la ciudad
    plt.savefig(f'barras_propietarios_{nombre_ciudad}.png')
    plt.show()

# Definimos las rutas de los archivos CSV para Madrid y Barcelona
madrid_data = '../listings_madrid.csv'
barcelona_data = '../listings_barcelona.csv'

# Generamos los informes para Madrid y Barcelona
generar_informe_propietarios(madrid_data, 'Madrid')
generar_informe_propietarios(barcelona_data, 'Barcelona')