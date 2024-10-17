// Capa del mapa de categorías
categLayer = null;

// Función para asignar colores según el tipo de alojamiento
function getColor(roomType) {
  switch (roomType) {
    case "Entire home/apt":
      return "blue";
    case "Private room":
      return "orange";
    case "Shared room":
      return "green";
    case "Hotel room":
      return "red";
    default:
      return "gray";
  }
}

// Función para definir cómo se verá cada punto en el mapa
function pointToLayer(feature, latlng) {
  return L.circleMarker(latlng, {
    radius: 5,
    fillColor: getColor(feature.properties.room_type),
    color: "#000",
    weight: 1,
    opacity: 1,
    fillOpacity: 0.8,
  });
}

// Generar mapa de categorías
Promise.all([
  fetch("./data/madrid_roomtype.geojson").then((response) => response.json()),
  fetch("./data/barcelona_roomtype.geojson").then((response) => response.json())
])
  .then((data) => {
    // Crear una capa única que contenga los datos de ambas ciudades
    categLayer = L.geoJSON(data[0], {
      pointToLayer: pointToLayer,
      onEachFeature: function (feature, layer) {
        // Pop-up al hacer clic en un punto
        layer.bindPopup(
          `<strong>${feature.properties.name}</strong><br>Tipo: ${feature.properties.room_type}`
        );
      },
    });

    // Añadir el GeoJSON de Barcelona a la misma capa
    categLayer.addData(data[1]);

    // Añadir la capa combinada al mapa
    categLayer.addTo(map);
  })
  .catch();

// Detectar cambios de visibilidad de capas
document.addEventListener("DOMContentLoaded", function () {
  const layerItems = document.querySelectorAll(".layers li");

  layerItems.forEach((item) => {
    item.addEventListener("click", function () {
      // Si el mapa se está centrando, ignorar función
      if (moving) return;

      item.classList.toggle("visible");
      item.querySelector("i").classList.toggle("fa-eye");
      item.querySelector("i").classList.toggle("fa-eye-slash");

      // Seleccionar la capa
      id = item.getAttribute("id");
      layer = null;
      switch (id) {
        case "categ":
          layer = categLayer;
          break;
        default:
      }

      // Cambiar la visibilidad de la capa si se ha encontrado
      if (layer !== null) toggleLayerView(layer);
    });
  });
});
