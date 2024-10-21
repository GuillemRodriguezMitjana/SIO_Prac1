// Función para cambiar la intensidad del mapa de calor en función del precio
function updateHeatMap(intensity) {
  // Ignorar cambio en caso de que no haya terminado uno previo
  if (changingIntensity) return;
  else changingIntensity = true;

  // Limpiar la capa de calor actual
  if (heatLayer) map.removeLayer(heatLayer);

  // Generar nuevo mapa de calor
  Promise.all([
    fetch("./data/madrid_price.geojson").then((response) => response.json()),
    fetch("./data/barcelona_price.geojson").then((response) => response.json()),
  ])
    .then(([madridData, barcelonaData]) => {
      // Combinar los datos de ambas ciudades
      const heatData = [];

      // Procesar datos de Madrid
      madridData.features.forEach((feature) => {
        heatData.push([
          feature.geometry.coordinates[1], // Latitud
          feature.geometry.coordinates[0], // Longitud
          feature.properties.price / intensity, // Intensidad basada en el precio
        ]);
      });

      // Procesar datos de Barcelona
      barcelonaData.features.forEach((feature) => {
        heatData.push([
          feature.geometry.coordinates[1], // Latitud
          feature.geometry.coordinates[0], // Longitud
          feature.properties.price / intensity, // Intensidad basada en el precio
        ]);
      });

      // Crear la capa de calor combinada y añadirla al mapa
      heatLayer = L.heatLayer(heatData, {
        radius: 20,
        blur: 0,
        maxZoom: 19,
      }).addTo(map);

      changingIntensity = false;
    })
    .catch(() => (changingIntensity = false));
}

// Función para cambiar la visibilidad de la capa de calor
function changeLayerView(button) {
  // Ignorar si el mapa se está centrando
  if (moving) return;

  // Cambiar estilos
  button.classList.toggle("visible");
  button.querySelector("i").classList.toggle("fa-eye");
  button.querySelector("i").classList.toggle("fa-eye-slash");

  // Cambiar la visibilidad
  toggleLayerView(heatLayer);
}

// MAIN ------------------------------------------------------------------------------------

// Capa del mapa de calor
heatLayer = null;

// Variable para indicar que se está cambiando la intensidad
changingIntensity = false;

// DOMs del slider
const priceSlider = document.getElementById("priceSlider");
const priceValue = document.getElementById("priceValue");

// Primera inicialización del mapa
updateHeatMap(priceSlider.value);
priceValue.innerHTML = priceSlider.value;

// Detectar el cambio de intensidad
priceSlider.addEventListener("change", () => {
  updateHeatMap(priceSlider.value);
});
priceSlider.addEventListener("input", () => {
  priceValue.innerHTML = priceSlider.value;
});
