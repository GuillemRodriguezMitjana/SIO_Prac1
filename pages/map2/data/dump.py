import pandas as pd
import json

def dataframe_to_geojson(df, output_filename):
    # Convierte un DataFrame a formato GeoJSON y lo guarda en un archivo
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    # Recorremos cada fila del DataFrame y construimos las 'features' del GeoJSON
    for _, row in df.iterrows():
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row['longitude'], row['latitude']]
            },
            "properties": {
                "room_type": row["room_type"],  # Tipo de habitación
                "name": row["name"]  # Nombre del alojamiento
            }
        }
        geojson["features"].append(feature)

    # Guardamos el GeoJSON en el archivo de salida
    with open(output_filename, "w") as f:
        json.dump(geojson, f, indent=2)

# Cargamos los datos de los CSV correspondientes
df_madrid = pd.read_csv("../../../data/listings_madrid.csv")
df_barcelona = pd.read_csv("../../../data/listings_barcelona.csv")

# Creamos los archivos GeoJSON
dataframe_to_geojson(df_madrid, "madrid_roomtype.geojson")
dataframe_to_geojson(df_barcelona, "barcelona_roomtype.geojson")