// Capa del mapa de burbujas
let bubbleLayer = null;

changingScale = false;

// Función para calcular el radio de la burbuja según la escala y el conteo
function getRadius(count, scale) {
  return Math.sqrt(count / 10) * scale;
}

// Función para actualizar las burbujas en el mapa
function updateBubbleMap(scale) {
  // Ignorar cambio en caso de que no haya terminado uno previo
  if (changingScale) return;
  else changingScale = true;

  // Limpiar la capa de burbujas actual
  if (bubbleLayer) map.removeLayer(bubbleLayer);

  // Generar nuevo mapa de burbujas
  Promise.all([
    fetch("./data/madrid_bubble.geojson").then((res) => res.json()),
    fetch("./data/barcelona_bubble.geojson").then((res) => res.json()),
  ])
    .then(([madridData, barcelonaData]) => {
      // Combinar los datos de ambas ciudades
      const combinedData = [...madridData.features, ...barcelonaData.features];

      // Crear mapa de burbujas
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
            `<div class="popup">
              <h3>${feature.properties.neighbourhood_group}</h3>
              <div>
                  <i class="fa-solid fa-building"></i>
                  <p>${feature.properties.count}</p>
              </div>
            </div>`
          );
        },
      }).addTo(map);

      changingScale = false;
    })
    .catch(() => (changingScale = false));
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

const scaleSlider = document.getElementById("scaleSlider");
const scaleValue = document.getElementById("scaleValue");

// Primera inicialización del mapa
updateBubbleMap(scaleSlider.value);
scaleValue.innerHTML = scaleSlider.value;

// Detectar el cambio de escala
scaleSlider.addEventListener("change", () => {
  updateBubbleMap(scaleSlider.value);
});
scaleSlider.addEventListener("input", () => {
  scaleValue.textContent = scaleSlider.value;
});
