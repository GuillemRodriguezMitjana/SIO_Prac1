import pandas as pd
import json

# Coordenadas centro de los distritos de Madrid y Barcelona
district_coords = {
    "Madrid": {
        "Centro": [40.41774, -3.70643],
        "Chamberí": [40.43891, -3.70574],
        "Salamanca": [40.42670, -3.68076],
        "Tetuán": [40.46053, -3.69836],
        "Arganzuela": [40.39650, -3.69707],
        "Carabanchel": [40.37441, -3.74462],
        "Ciudad Lineal": [40.44838, -3.65038],
        "Retiro": [40.41075, -3.67596],
        "Chamartín": [40.45883, -3.67596],
        "Puente de Vallecas": [40.39807, -3.66875],
        "Latina": [40.4028, -3.7357],
        "Moncloa - Aravaca": [40.4558, -3.7807],
        "Usera": [40.38369, -3.70651],
        "San Blas - Canillejas": [40.4313, -3.6124],
        "Hortaleza": [40.47229, -3.64214],
        "Fuencarral - El Pardo": [40.5488, -3.7072],
        "Villaverde": [40.34497, -3.69570],
        "Moratalaz": [40.40591, -3.64437],
        "Barajas": [40.4725, -3.5802],
        "Villa de Vallecas": [40.3732, -3.6118],
        "Vicálvaro": [40.4017, -3.5956],
    },
    "Barcelona": {
        "Eixample": [41.39349, 2.16388],
        "Ciutat Vella": [41.38164, 2.18036],
        "Sants-Montjuïc": [41.36869, 2.14457],
        "Sant Martí": [41.40823, 2.20276],
        "Gràcia": [41.40649, 2.15838],
        "Sarrià-Sant Gervasi": [41.398611, 2.131111],
        "Horta-Guinardó": [41.42896, 2.15057],
        "Les Corts": [41.38499, 2.13289],
        "Sant Andreu": [41.43732, 2.19589],
        "Nou Barris": [41.44517, 2.17907],
    }
}

# Función para crear un GeoJSON a partir de un DataFrame y coordenadas
def dataframe_to_geojson(df, coords, output_filename):
    # Inicializar el GeoJSON
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    # Crear features para cada distrito con sus coordenadas
    for _, row in df.iterrows():
        district = row["neighbourhood_group_cleansed"]
        if district in coords:
            lat, lon = coords[district]
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                },
                "properties": {
                    "neighbourhood_group": district,
                    "count": row["count"]
                }
            }
            geojson["features"].append(feature)

    # Guardar el GeoJSON en un archivo
    with open(output_filename, "w") as f:
        json.dump(geojson, f, indent=2)

# Cargar los datos
df_madrid = pd.read_csv("../../../data/listings_madrid.csv")
df_barcelona = pd.read_csv("../../../data/listings_barcelona.csv")

# Agrupar por distrito y contar el número de alojamientos
def count_accommodations(df):
    return df.groupby("neighbourhood_group_cleansed").size().reset_index(name="count")

# Obtener los DataFrames con los conteos
df_madrid_counts = count_accommodations(df_madrid)
df_barcelona_counts = count_accommodations(df_barcelona)

# Crear los archivos GeoJSON
dataframe_to_geojson(df_madrid_counts, district_coords["Madrid"], "madrid_bubbles.geojson")
dataframe_to_geojson(df_barcelona_counts, district_coords["Barcelona"], "barcelona_bubbles.geojson")
