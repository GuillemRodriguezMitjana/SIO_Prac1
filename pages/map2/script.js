// Inicializar el mapa centrado en España
const map2 = L.map("map").setView([40.4168, -3.7038], 6); // Centrado en España

// Añadir capa base de OpenStreetMap
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution: "© OpenStreetMap",
}).addTo(map2);

// Función para asignar colores según el tipo de alojamiento
function getColor(roomType) {
  switch (roomType) {
    case "Entire home/apt":
      return "blue";
    case "Private room":
      return "green";
    case "Shared room":
      return "red";
    case "Hotel room":
      return "purple";
    default:
      return "gray"; // Color por defecto para casos no contemplados
  }
}

// Función para definir cómo se verá cada punto en el mapa
function pointToLayer(feature, latlng) {
  return L.circleMarker(latlng, {
    radius: 8, // Tamaño del punto
    fillColor: getColor(feature.properties.room_type), // Color según room_type
    color: "#000", // Borde del punto
    weight: 1,
    opacity: 1,
    fillOpacity: 0.8,
  });
}

// Cargar y añadir GeoJSON de Madrid
fetch("./data/madrid_roomtype.geojson")
  .then((response) => response.json())
  .then((data) => {
    L.geoJSON(data, {
      pointToLayer: pointToLayer, // Define cómo se renderizan los puntos
      onEachFeature: function (feature, layer) {
        // Pop-up al hacer clic en un punto
        layer.bindPopup(
          `<strong>${feature.properties.name}</strong><br>Tipo: ${feature.properties.room_type}`
        );
      },
    }).addTo(map2);
  });

// Cargar y añadir GeoJSON de Barcelona
fetch("./data/barcelona_roomtype.geojson")
  .then((response) => response.json())
  .then((data) => {
    L.geoJSON(data, {
      pointToLayer: pointToLayer, // Usa la misma configuración de puntos
      onEachFeature: function (feature, layer) {
        // Pop-up al hacer clic en un punto
        layer.bindPopup(
          `<strong>${feature.properties.name}</strong><br>Tipo: ${feature.properties.room_type}`
        );
      },
    }).addTo(map2);
  });
