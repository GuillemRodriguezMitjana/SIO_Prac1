let bubbleLayer = null;

// Función para centrar el mapa
function centerMap(lat, lng, zoom) {
  map.setView([lat, lng], zoom);
}

// Función para calcular el radio de la burbuja según la escala y el conteo
function getRadius(count, scale) {
  return Math.sqrt(count) * scale;
}

// Función para actualizar las burbujas en el mapa
function updateBubbleMap(scale) {
  if (bubbleLayer) map.removeLayer(bubbleLayer);

  Promise.all([
    fetch("./data/madrid_bubble.geojson").then((res) => res.json()),
    fetch("./data/barcelona_bubble.geojson").then((res) => res.json()),
  ])
    .then(([madridData, barcelonaData]) => {
      const combinedData = [...madridData.features, ...barcelonaData.features];

      bubbleLayer = L.geoJSON(combinedData, {
        pointToLayer: function (feature, latlng) {
          const radius = getRadius(feature.properties.count, scale);
          return L.circleMarker(latlng, {
            radius: radius,
            fillColor: "blue",
            color: "#000",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.6,
          });
        },
        onEachFeature: function (feature, layer) {
          layer.bindPopup(
            `<div class="popup"><strong>${feature.properties.neighbourhood_group}</strong><br>
              Alojamientos: ${feature.properties.count}</div>`
          );
        },
      }).addTo(map);
    });
}

// Función para poner y quitar las burbujas
function changeLayerView(button) {
  // Ignorar si el mapa se está centrando
  if (moving) return;

  // Cambiar estilos
  button.classList.toggle("visible");
  button.querySelector("i").classList.toggle("fa-eye");
  button.querySelector("i").classList.toggle("fa-eye-slash");

  // Cambiar
  toggleLayerView(bubbleLayer);
}

// Inicializar el mapa con escala predeterminada
const scaleSlider = document.getElementById("scaleSlider");
const scaleValue = document.getElementById("scaleValue");
updateBubbleMap(scaleSlider.value);

// Actualizar la escala al mover el slider
scaleSlider.addEventListener("change", () => {
  updateBubbleMap(scaleSlider.value);
});
scaleSlider.addEventListener("input", () => {
  scaleValue.textContent = scaleSlider.value;
});
