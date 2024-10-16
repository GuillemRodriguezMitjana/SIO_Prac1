// Inicializar el mapa centrado en España
const map = L.map("map").setView([40.4168, -3.7038], 6); // Centrado en España

// Añadir capa base de OpenStreetMap
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution: "© OpenStreetMap",
}).addTo(map);

// Cargar y añadir GeoJSON de Madrid
fetch("./data/madrid_price.geojson")
  .then((response) => response.json())
  .then((data) => {
    const heatDataMadrid = data.features.map((feature) => [
      feature.geometry.coordinates[1], // Latitud
      feature.geometry.coordinates[0], // Longitud
      feature.properties.price / 500, // Intensidad basada en el precio
    ]);
    const heat = L.heatLayer(heatDataMadrid, {
      radius: 20,
      blur: 15,
      maxZoom: 19,
    }).addTo(map);
  });

// Cargar y añadir GeoJSON de Barcelona
fetch("./data/barcelona_price.geojson")
  .then((response) => response.json())
  .then((data) => {
    const heatDataBarcelona = data.features.map((feature) => [
      feature.geometry.coordinates[1], // Latitud
      feature.geometry.coordinates[0], // Longitud
      feature.properties.price / 500, // Intensidad basada en el precio
    ]);
    const heat = L.heatLayer(heatDataBarcelona, {
      radius: 20,
      blur: 15,
      maxZoom: 19,
    }).addTo(map);
  });
