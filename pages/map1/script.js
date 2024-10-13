// Inicializar el mapa
const map = L.map("map").setView([40.4168, -3.7038], 6);

// Capa de mapa
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution: "© OpenStreetMap",
}).addTo(map);

// Cargar y añadir el GeoJSON de Madrid
fetch("../../data/neighbourhoods_madrid.geojson")
  .then((response) => response.json())
  .then((data) => {
    L.geoJSON(data, {
      style: function (feature) {
        return { color: "blue", weight: 2 }; // Estilo para Madrid
      },
      onEachFeature: function (feature, layer) {
        layer.bindPopup(
          `<h3>${feature.properties.neighbourhood_group}</h3><p>${feature.properties.neighbourhood}</p>`
        );
      },
    }).addTo(map);
  });

// Cargar y añadir el GeoJSON de Barcelona
fetch("../../data/neighbourhoods_barcelona.geojson")
  .then((response) => response.json())
  .then((data) => {
    L.geoJSON(data, {
      style: function (feature) {
        return { color: "orange", weight: 2 }; // Estilo para Barcelona
      },
      onEachFeature: function (feature, layer) {
        layer.bindPopup(
          `<h3>${feature.properties.neighbourhood_group}</h3><p>${feature.properties.neighbourhood}</p>`
        );
      },
    }).addTo(map);
  });
