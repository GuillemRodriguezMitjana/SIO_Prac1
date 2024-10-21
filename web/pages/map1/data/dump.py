import pandas as pd
import json

# Función para limpiar la columna de precios
def clean_price_column(df):
    df['price'] = pd.to_numeric(df['price'].replace({'\$': '', ',': ''}, regex=True), errors='coerce')
    df = df.dropna(subset=['price'])
    return df

# Cargar los datos
df_madrid = pd.read_csv("../../../data/listings_madrid.csv")
df_barcelona = pd.read_csv("../../../data/listings_barcelona.csv")

# Limpiar la columna de precios
df_madrid = clean_price_column(df_madrid)
df_barcelona = clean_price_column(df_barcelona)

# Función para crear el GeoJSON
def dataframe_to_geojson(df, output_filename):
    # Inicializar el GeoJSON
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    # Recorrer cada alojamiento y construir su GeoJSON
    for _, row in df.iterrows():
        geojson["features"].append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row['longitude'], row['latitude']]
            },
            "properties": {
                "price": row["price"]
            }
        })

    # Guardar el GeoJSON
    with open(output_filename, "w") as f:
        json.dump(geojson, f, indent=2)

# Crear archivos GeoJSON
dataframe_to_geojson(df_madrid, "madrid_price.geojson")
dataframe_to_geojson(df_barcelona, "barcelona_price.geojson")