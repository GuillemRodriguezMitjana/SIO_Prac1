// Cambiar TMS por defecto
changeMapLayer("stamen-toner");

// Capa del mapa de tráfico
trafficLayer = null;

Promise.all([
  fetch("./data/madrid_connections.geojson").then((response) =>
    response.json()
  ),
  fetch("./data/barcelona_connections.geojson").then((response) =>
    response.json()
  ),
])
  .then(([madridData, barcelonaData]) => {
    // Combinar ambos GeoJSON en un solo array de features
    const combinedFeatures = madridData.features.concat(barcelonaData.features);

    // Crear una nueva capa GeoJSON con los datos combinados
    trafficLayer = L.geoJSON(
      { type: "FeatureCollection", features: combinedFeatures },
      {
        style: function (feature) {
          return {
            color: "blue", // Color de las líneas
            weight: 2, // Grosor de las líneas
            opacity: 0.8, // Transparencia
          };
        },
        onEachFeature: function (feature, layer) {
          // Añadir un popup para mostrar la información del host y del barrio del alojamiento
          if (feature.properties) {
            layer.bindPopup(
              `<b>Host:</b> ${feature.properties.host_neighbourhood}<br>` +
                `<b>Alojamiento en:</b> ${feature.properties.alojamiento_neighbourhood}<br>` +
                `<b>Ciudad:</b> ${feature.properties.ciudad}`
            );
          }
        },
      }
    );

    // Añadir la capa de tráfico al mapa
    trafficLayer.addTo(map);
  })
  .catch();
