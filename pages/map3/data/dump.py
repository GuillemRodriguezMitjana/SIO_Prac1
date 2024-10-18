import json
import pandas as pd
import numpy as np

# Función para limpiar la columna de precios
def clean_price_column(df):
    df['price'] = df['price'].replace({'\$': '', ',': ''}, regex=True).astype(float)
    return df

# Cargar los datos
madrid_data = pd.read_csv('../../../data/listings_madrid.csv')
barcelona_data = pd.read_csv('../../../data/listings_barcelona.csv')

# Limpiar la columna de precios
madrid_data = clean_price_column(madrid_data)
barcelona_data = clean_price_column(barcelona_data)

# Agrupar los datos por distritos y calcular estadísticas
def calcular_estadisticas_por_distrito(df, neighbourhood):
    stats = df.groupby(neighbourhood).agg({
        'price': ['mean', 'min', 'max'],
        'id': 'count',
        'number_of_reviews': 'mean',
        'review_scores_rating': 'mean',
        'review_scores_location': 'mean',
    }).reset_index()

    # Renombrar las columnas resultantes
    stats.columns = ['neighbourhood_cleansed', 'precio_medio', 'precio_min', 'precio_max', 
                     'total_alojamientos', 'promedio_reseñas', 'valoracion_media', 
                     'valoracion_ubicacion']
    
    return stats

# Calcular estadísticas
madrid_stats = calcular_estadisticas_por_distrito(madrid_data, 'neighbourhood_cleansed')
barcelona_stats = calcular_estadisticas_por_distrito(barcelona_data, 'neighbourhood_cleansed')

# Función para reemplazar NaNs por None
def safe_value(value):
    if pd.isna(value) or np.isnan(value):
        return None
    return float(value)

# Función para generar el GeoJSON
def enriquecer_geojson(geojson_file, stats_df, neighbourhood):
    with open(geojson_file, 'r') as f:
        geojson_data = json.load(f)

    for feature in geojson_data['features']:
        neighbourhood_name = feature['properties']['neighbourhood']
        
        # Buscar el distrito en los datos de estadísticas
        match = stats_df[stats_df[neighbourhood] == neighbourhood_name]
        
        if not match.empty:
            feature['properties']['precio_medio'] = safe_value(match['precio_medio'].values[0])
            feature['properties']['precio_min'] = safe_value(match['precio_min'].values[0])
            feature['properties']['precio_max'] = safe_value(match['precio_max'].values[0])
            feature['properties']['total_alojamientos'] = safe_value(match['total_alojamientos'].values[0])
            feature['properties']['promedio_reseñas'] = safe_value(match['promedio_reseñas'].values[0])
            feature['properties']['valoracion_media'] = safe_value(match['valoracion_media'].values[0])
            feature['properties']['valoracion_ubicacion'] = safe_value(match['valoracion_ubicacion'].values[0])
        else:
            feature['properties']['info'] = 'Sin información'

    return geojson_data

# Crear los GeoJSON
madrid_geojson = enriquecer_geojson('../../../data/neighbourhoods_madrid.geojson', madrid_stats, 'neighbourhood_cleansed')
barcelona_geojson = enriquecer_geojson('../../../data/neighbourhoods_barcelona.geojson', barcelona_stats, 'neighbourhood_cleansed')

# Guardar los nuevos GeoJSON
with open('madrid_neighbourhood.geojson', 'w') as f:
    json.dump(madrid_geojson, f)

with open('barcelona_neighbourhood.geojson', 'w') as f:
    json.dump(barcelona_geojson, f)
