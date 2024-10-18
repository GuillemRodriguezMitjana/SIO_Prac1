// TMS por defecto
changeMapLayer("worldimagery");

// Capa del mapa de coropletas
choroplethLayer = null;

// Función para asignar colores en función del precio medio
function getColor(price) {
  if (price > 200) return "#ff0000";
  else if (price < 50) return "#ffff00";
  else return "#00ff00";
}

// Generar mapa de coropletas
Promise.all([
  fetch("./data/madrid_neighbourhood.geojson").then((response) =>
    response.json()
  ),
  fetch("./data/barcelona_neighbourhood.geojson").then((response) =>
    response.json()
  ),
])
  .then(([dataMadrid, dataBarcelona]) => {
    choroplethLayer = L.geoJSON(null, {
      style: function (feature) {
        return {
          fillColor: getColor(feature.properties.precio_medio),
          weight: 1,
          opacity: 1,
          color: "black",
          fillOpacity: 0.3,
        };
      },
      onEachFeature: function (feature, layer) {
        const popupContent = `
            <b>${feature.properties.neighbourhood}</b><br>
            Precio medio: ${
              feature.properties.precio_medio || "No disponible"
            }<br>
            Total alojamientos: ${
              feature.properties.total_alojamientos || "No disponible"
            }<br>
            Valoración ubicación: ${
              feature.properties.valoracion_ubicacion || "No disponible"
            }
        `;
        layer.bindPopup(popupContent);
      },
    });

    choroplethLayer.addData(dataMadrid);
    choroplethLayer.addData(dataBarcelona);

    choroplethLayer.addTo(map);
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
        case "choropleth":
          layer = choroplethLayer;
          break;
        default:
      }

      // Cambiar la visibilidad de la capa si se ha encontrado
      if (layer !== null) toggleLayerView(layer);
    });
  });
});
