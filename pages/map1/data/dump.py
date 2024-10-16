import pandas as pd
import json


def dataframe_to_geojson(df, output_filename):
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    for _, row in df.iterrows():
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row['longitude'], row['latitude']]
            },
            "properties": {
                "price": row["price"],
                "name": row["name"]
            }
        }
        geojson["features"].append(feature)

    with open(output_filename, "w") as f:
        json.dump(geojson, f, indent=2)


def clean_price_column(df):
    df['price'] = pd.to_numeric(df['price'].replace({'\$': '', ',': ''}, regex=True), errors='coerce')
    df = df.dropna(subset=['price'])
    return df


df_madrid = pd.read_csv("../../../data/listings_madrid.csv")
df_barcelona = pd.read_csv("../../../data/listings_barcelona.csv")

df_madrid = clean_price_column(df_madrid)
df_barcelona = clean_price_column(df_barcelona)

dataframe_to_geojson(df_madrid, "madrid_price.geojson")
dataframe_to_geojson(df_barcelona, "barcelona_price.geojson")