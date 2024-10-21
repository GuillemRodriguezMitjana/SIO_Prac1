# Biblioteca que facilita la manipulación de datos estructurados
import pandas as pd
# Biblioteca para crear gráficos y visualizaciones
import matplotlib.pyplot as plt

# Función que genera tabla de frecuencias y gráfica de pastel para una ciudad
def generar_informe(archivo_csv, nombre_ciudad):
    # Leemos el CSV y lo cargamos en un DataFrame
    datos = pd.read_csv(archivo_csv)
    # Contamos cuántas veces aparece cada distrito
    frecuencia = datos['neighbourhood_group_cleansed'].value_counts()
    # Convertimos la serie en un DataFrame y renombramos las columnas
    tabla_frecuencias = frecuencia.reset_index()
    tabla_frecuencias.columns = ['Distrito', 'Frecuencia']
    # Calculamos la frecuencia relativa y el porcentaje
    tabla_frecuencias['Frecuencia relativa'] = tabla_frecuencias['Frecuencia'] / tabla_frecuencias['Frecuencia'].sum()
    tabla_frecuencias['Porcentaje'] = tabla_frecuencias['Frecuencia relativa'] * 100
    # Redondeamos los decimales
    tabla_frecuencias['Frecuencia relativa'] = tabla_frecuencias['Frecuencia relativa'].round(3)
    tabla_frecuencias['Porcentaje'] = tabla_frecuencias['Porcentaje'].round(2)
    # Calculamos el total de alojamientos
    total_alojamientos = tabla_frecuencias['Frecuencia'].sum()
    # Creamos una fila con los totales
    total_fila = pd.DataFrame({'Distrito': ['TOTAL'], 'Frecuencia': [total_alojamientos]})
    total_fila['Frecuencia relativa'] = [1]
    total_fila['Porcentaje'] = [100]
    # Concatenamos la fila a la tabla
    tabla_frecuencias = pd.concat([tabla_frecuencias, total_fila], ignore_index=True)

    # Crear y mostrar la tabla en un gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('tight')
    ax.axis('off')
    tabla = ax.table(cellText=tabla_frecuencias.values, colLabels=tabla_frecuencias.columns, cellLoc='center', loc='center')
    # Ponemos en negrita los encabezados y la fila TOTAL
    for j in range(len(tabla_frecuencias.columns)):
        tabla[(0, j)].set_text_props(fontweight='bold')
    tabla[(len(tabla_frecuencias) - 1, 0)].set_text_props(fontweight='bold')
    # Ajustamos el tamaño de las columnas automáticamente
    tabla.auto_set_column_width(range(len(tabla_frecuencias.columns)))
    # Mostramos la tabla
    plt.show()

    # Crear y mostrar la gráfica de pastel
    plt.figure(figsize=(10, 6))
    plt.pie(tabla_frecuencias['Frecuencia'][:-1], labels=tabla_frecuencias['Distrito'][:-1], autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Asegura que el gráfico sea un círculo
    # Guardamos la gráfica con el nombre de la ciudad
    plt.savefig(f'distribucion_distritos_{nombre_ciudad}.png')
    plt.show()

# Leemos los archivos CSV de Madrid y Barcelona
madrid_data = '../listings_madrid.csv'
barcelona_data = '../listings_barcelona.csv'

# Generamos los informes para cada ciudad
generar_informe(madrid_data, 'Madrid')
generar_informe(barcelona_data, 'Barcelona')