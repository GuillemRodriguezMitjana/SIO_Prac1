import json
import pandas as pd
import numpy as np

# Función para calcular el centroide de un polígono (punto medio)
def calcular_centroide(polygon_coords):
    # Extraer las coordenadas
    coords = np.array(polygon_coords[0])  # Primer anillo del polígono (en caso de multipolígono)
    x_coords = coords[:, 0]
    y_coords = coords[:, 1]

    # Calcular el centroide (media aritmética de las coordenadas)
    centroide_x = np.mean(x_coords)
    centroide_y = np.mean(y_coords)
    
    return [centroide_x, centroide_y]

# Función para leer los GeoJSON de los barrios y obtener las coordenadas de cada barrio
def cargar_barrios_geojson(geojson_file):
    with open(geojson_file, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)

    barrios_coords = {}
    for feature in geojson_data['features']:
        barrio = feature['properties']['neighbourhood']
        coords = feature['geometry']['coordinates']
        barrios_coords[barrio] = calcular_centroide(coords)

    return barrios_coords

# Función para crear el GeoJSON de conexiones entre host y alojamientos
def crear_geojson_conexiones(data, barrios_coords, ciudad):
    geojson_conexiones = []

    for index, row in data.iterrows():
        host_barrio = row['host_neighbourhood']
        aloj_barrio = row['neighbourhood_cleansed']

        # Verificar si ambos barrios tienen coordenadas disponibles
        if host_barrio in barrios_coords and aloj_barrio in barrios_coords:
            host_coords = barrios_coords[host_barrio]
            aloj_coords = barrios_coords[aloj_barrio]

            # Crear una línea entre el barrio del host y el del alojamiento
            feature = {
                "type": "LineString",
                "coordinates": [host_coords, aloj_coords]
            }
            geojson_conexiones.append(feature)

    return geojson_conexiones

# Cargar los datos de los alojamientos
madrid_data = pd.read_csv('../../../data/listings_madrid.csv')
barcelona_data = pd.read_csv('../../../data/listings_barcelona.csv')

# Cargar los GeoJSON con los barrios y sus coordenadas
madrid_barrios_coords = cargar_barrios_geojson('../../../data/neighbourhoods_madrid.geojson')
barcelona_barrios_coords = cargar_barrios_geojson('../../../data/neighbourhoods_barcelona.geojson')

# Filtrar los datos necesarios
madrid_filtered = madrid_data[['host_neighbourhood', 'neighbourhood_cleansed']].dropna()
barcelona_filtered = barcelona_data[['host_neighbourhood', 'neighbourhood_cleansed']].dropna()

# Crear el GeoJSON de conexiones para Madrid y Barcelona
madrid_conexiones_geojson = crear_geojson_conexiones(madrid_filtered, madrid_barrios_coords, 'Madrid')
barcelona_conexiones_geojson = crear_geojson_conexiones(barcelona_filtered, barcelona_barrios_coords, 'Barcelona')

# Guardar los GeoJSON resultantes
with open('madrid_connections.geojson', 'w') as f:
    json.dump(madrid_conexiones_geojson, f)

with open('barcelona_connections.geojson', 'w') as f:
    json.dump(barcelona_conexiones_geojson, f)
