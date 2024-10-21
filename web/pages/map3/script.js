// Cambiar TMS por defecto
changeMapLayer("worldimagery");

// Capa del mapa de coropletas
choroplethLayer = null;

// Función para asignar colores en 5 rangos
let rango1, rango2, rango3, rango4, rango5;
function obtenerRangos(data) {
  // Limpiar datos
  data = data.filter((value) => typeof value === "number");

  // Calcular la media
  const media = data.reduce((a, b) => a + b, 0) / data.length;

  // Calcular la desviación estándar
  const desviacion = Math.sqrt(
    data.map((x) => Math.pow(x - media, 2)).reduce((a, b) => a + b, 0) /
      data.length
  );

  // Definir los límites de los rangos
  rango1 = media - 2 * desviacion;
  rango2 = media - desviacion;
  rango3 = media;
  rango4 = media + desviacion;
  rango5 = media + 2 * desviacion;
}

// Función para asignar colores según el rango
function getColor(value) {
  if (value === undefined) {
    return "#000";
  } else if (value <= rango1) {
    return "#00FF00";
  } else if (value <= rango2) {
    return "#66FF00";
  } else if (value <= rango3) {
    return "#FFFF00";
  } else if (value <= rango4) {
    return "#FF9900";
  } else if (value <= rango5) {
    return "#FF0000";
  } else {
    return "#880000";
  }
}

changingOpacity = false;

// Función para cambiar la opacidad del mapa de coropletas
function updateChoroplethMap(opacity, type = "precio_medio") {
  // Ignorar si aún no ha terminado un cambio previo
  if (changingOpacity) return;
  else changingOpacity = true;

  // Limpiar la capa de coropletas actual
  if (choroplethLayer) map.removeLayer(choroplethLayer);

  // Generar nuevo mapa de coropletas
  Promise.all([
    fetch("./data/madrid_neighbourhood.geojson").then((response) =>
      response.json()
    ),
    fetch("./data/barcelona_neighbourhood.geojson").then((response) =>
      response.json()
    ),
  ])
    .then(([dataMadrid, dataBarcelona]) => {
      // Crear la capa de coropletas
      choroplethLayer = L.geoJSON(null, {
        style: function (feature) {
          return {
            fillColor: getColor(feature.properties[type]),
            weight: 1,
            opacity: 1,
            color: "black",
            fillOpacity: opacity / 100,
          };
        },
        onEachFeature: function (feature, layer) {
          const popupContent = `
            <div class="nh-card">
              <h1>${feature.properties.neighbourhood_group}</h1>
              <h2>${feature.properties.neighbourhood}</h2>
              <div class="nh-info">
                <div>
                  <i class="fa-solid fa-coins"></i>
                  <p>${feature.properties.precio_medio}</p>
                </div>
                <div>
                  <i class="fa-solid fa-building"></i>
                  <p>${feature.properties.total_alojamientos}</p>
                </div>
                <div>
                  <i class="fa-solid fa-comments"></i>
                  <p>${feature.properties.promedio_reseñas}</p>
                </div>
                <div>
                  <i class="fa-solid fa-star"></i>
                  <p>${feature.properties.valoracion_media}</p>
                </div>
                <div>
                  <i class="fa-solid fa-star-half-stroke"></i>
                  <p>${feature.properties.valoracion_ubicacion}</p>
                </div>
              </div>
            </div>
          `;
          layer.bindPopup(popupContent);
        },
      });

      // Juntar los datos de las dos ciudades para obtener los rangos
      let dataOfType = [];
      dataMadrid.features.forEach((feature) => {
        dataOfType.push(feature.properties[type]);
      });
      dataBarcelona.features.forEach((feature) => {
        dataOfType.push(feature.properties[type]);
      });
      obtenerRangos(dataOfType);

      // Añadir datos a la capa de coropletas
      choroplethLayer.addData(dataMadrid);
      choroplethLayer.addData(dataBarcelona);

      // Añadir capa al mapa
      choroplethLayer.addTo(map);

      changingOpacity = false;
    })
    .catch(() => (changingOpacity = false));
}

const opacitySlider = document.getElementById("opacitySlider");
const opacityValue = document.getElementById("opacityValue");

// Primera inicialización del mapa
updateChoroplethMap(opacitySlider.value);
opacityValue.innerHTML = opacitySlider.value;

// Detectar el cambio de opacidad
opacitySlider.addEventListener("change", () => {
  updateChoroplethMap(
    opacitySlider.value,
    document.querySelector(".func-selected").getAttribute("id")
  );
});
opacitySlider.addEventListener("input", () => {
  opacityValue.innerHTML = opacitySlider.value;
});

// Función para cambiar la distribución
function changeFunctionality(funct) {
  // Ignorar si el mapa se está centrando
  if (moving) return;

  // Ignorar si la funcionalidad seleccionada es la que ya está activa
  button = document.getElementById(funct);
  if (button.classList.contains("func-selected")) return;

  // Cambiar estilos
  funcItems = document.querySelectorAll(".funcs-list button");
  funcItems.forEach((item) => item.classList.remove("func-selected"));
  button.classList.add("func-selected");

  // Cambiar la funcionalidad
  updateChoroplethMap(opacitySlider.value, funct);
}
