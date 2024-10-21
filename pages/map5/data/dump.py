import json
import pandas as pd
import random

# Función para obtener los 5 hosts con más alojamientos
def obtener_top_hosts(data, n=5):
    # Contar el número de alojamientos por host
    host_counts = data['host_id'].value_counts()
    # Seleccionar los n hosts con más alojamientos
    top_hosts = host_counts.nlargest(n).index.tolist()
    return data[data['host_id'].isin(top_hosts)]

# Cargar los datos de los alojamientos
madrid_data = pd.read_csv('../../../data/listings_madrid.csv')
barcelona_data = pd.read_csv('../../../data/listings_barcelona.csv')

# Filtrar los datos necesarios y obtener los 5 hosts aleatorios con al menos 1 alojamiento
madrid_filtered = madrid_data[['latitude', 'longitude', 'host_id', 'host_url', 'host_name', 'host_since', 'host_response_time', 'host_response_rate', 'host_acceptance_rate', 'host_picture_url', 'host_identity_verified', 'listing_url']].dropna()
barcelona_filtered = barcelona_data[['latitude', 'longitude', 'host_id', 'host_url', 'host_name', 'host_since', 'host_response_time', 'host_response_rate', 'host_acceptance_rate', 'host_picture_url', 'host_identity_verified', 'listing_url']].dropna()

madrid_random_hosts = obtener_top_hosts(madrid_filtered, 5)
barcelona_random_hosts = obtener_top_hosts(barcelona_filtered, 5)

# Crear GeoJSON de alojamientos
def crear_geojson_puntos(data, city):
    geojson_puntos = {
        "type": "FeatureCollection",
        "features": []
    }

    for _, row in data.iterrows():
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row['longitude'], row['latitude']]
            },
            "properties": {
                "host_id": row['host_id'],
                "host_url": row['host_url'],
                "host_name": row['host_name'],
                "host_since": row['host_since'],
                "host_response_time": row['host_response_time'],
                "host_response_rate": row['host_response_rate'],
                "host_acceptance_rate": row['host_acceptance_rate'],
                "host_picture_url": row['host_picture_url'],
                "host_identity_verified": row['host_identity_verified'],
                "listing_url": row['listing_url'],
                "city": city
            }
        }
        geojson_puntos['features'].append(feature)

    return geojson_puntos

# Crear GeoJSON para Madrid y Barcelona
madrid_geojson = crear_geojson_puntos(madrid_random_hosts, "Madrid")
barcelona_geojson = crear_geojson_puntos(barcelona_random_hosts, "Barcelona")

# Guardar los GeoJSON resultantes
with open('madrid_hosts.geojson', 'w') as f:
    json.dump(madrid_geojson, f)

with open('barcelona_hosts.geojson', 'w') as f:
    json.dump(barcelona_geojson, f)
