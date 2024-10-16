// Capa del mapa de calor
heatLayer = null;

// Generar mapa de calor
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
        feature.properties.price / 200, // Intensidad basada en el precio
      ]);
    });

    // Procesar datos de Barcelona
    barcelonaData.features.forEach((feature) => {
      heatData.push([
        feature.geometry.coordinates[1], // Latitud
        feature.geometry.coordinates[0], // Longitud
        feature.properties.price / 200, // Intensidad basada en el precio
      ]);
    });

    // Crear la capa de calor combinada y añadirla al mapa
    heatLayer = L.heatLayer(heatData, {
      radius: 20,
      blur: 0,
      maxZoom: 19,
    }).addTo(map);
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
        case "heat":
          layer = heatLayer;
          break;
        default:
      }

      // Cambiar la visibilidad de la capa si se ha encontrado
      if (layer !== null) toggleLayerView(layer);
    });
  });
});
