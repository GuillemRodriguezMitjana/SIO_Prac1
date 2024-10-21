// Función para generar un color hexadecimal aleatorio
function getRandomColor() {
  let letters = "0123456789ABCDEF";
  let color = "#";
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

// Función para obtener un color único basado en el host_id
function getColor(hostId) {
  // Si el host no tiene ningún color asignado
  if (!hostColors[hostId]) {
    // Generar un color aleatorio y asignar
    let newColor = getRandomColor();
    hostColors[hostId] = newColor;
  }
  return hostColors[hostId];
}

// Función para actualizar el radio de los puntos en el mapa
function updateCategoryMap(radius) {
  // Ignorar cambio en caso de que no haya terminado uno previo
  if (changingRadius) return;
  else changingRadius = true;

  // Limpiar la capa de categorías actual
  if (categoryLayer) map.removeLayer(categoryLayer);

  // Diccionarios para contar el número de alojamientos de cada distrito en ambas ciudades
  madridCount = {};
  barcelonaCount = {};

  // Generar nuevo mapa de categorías
  Promise.all([
    fetch("./data/madrid_hosts.geojson").then((response) => response.json()),
    fetch("./data/barcelona_hosts.geojson").then((response) => response.json()),
  ])
    .then(([madridData, barcelonaData]) => {
      // Combinar los datos de ambas ciudades
      const combinedData = {
        type: "FeatureCollection",
        features: [...madridData.features, ...barcelonaData.features],
      };

      // Crear mapa de categorías
      categoryLayer = L.geoJSON(combinedData, {
        pointToLayer: (feature, latlng) => {
          // Asignar color según el host_id
          return L.circleMarker(latlng, {
            radius: radius, // Tamaño del marcador
            fillColor: getColor(feature.properties.host_id),
            color: "#000",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.7,
          });
        },
        onEachFeature: (feature, layer) => {
          // Guardar el id asociado de cada host
          hostNames[feature.properties.host_id] = feature.properties.host_name;

          // Incrementar el contador de alojamientos de cada host
          switch (feature.properties.city) {
            case "Madrid":
              if (madridCount[feature.properties.host_id])
                madridCount[feature.properties.host_id] += 1;
              else madridCount[feature.properties.host_id] = 1;
              break;
            case "Barcelona":
              if (barcelonaCount[feature.properties.host_id])
                barcelonaCount[feature.properties.host_id] += 1;
              else barcelonaCount[feature.properties.host_id] = 1;
              break;
            default:
          }

          // Añadir icono si el host está verificado
          const verified =
            feature.properties.host_identity_verified == "t"
              ? "#FF385C"
              : "transparent";

          // Popup con información del host
          layer.bindPopup(`
            <div class="host-card">
              <p class="host-since">${feature.properties.host_since}</p>
              <div class="host-name-container">
                <i class="fa-solid fa-circle-check" style="color: ${verified}"></i>
                <h3>${feature.properties.host_name}</h3>
              </div>
              <img src="${feature.properties.host_picture_url}"></img>
              <div class="host-info">
                <div>
                  <i class="fa-solid fa-reply"></i>
                  <p>${feature.properties.host_response_rate}</p>
                </div>
                <div>
                  <i class="fa-solid fa-clipboard-check"></i>
                  <p>${feature.properties.host_acceptance_rate}</p>
                </div>
                <div>
                  <i class="fa-solid fa-clock"></i>
                  <p>${feature.properties.host_response_time}</p>
                </div>
              </div>
              <div class="host-links">
                <a href="${feature.properties.host_url}" target="_blank">
                  <i class="fa-solid fa-user"></i>
                </a>
                <a href="${feature.properties.listing_url}" target="_blank">
                  <i class="fa-solid fa-building"></i>
                </a>
              </div>
            </div>`);
        },
      }).addTo(map);

      // Ordenador contador de alojamientos de Madrid
      let sortedMadridCount = Object.entries(madridCount).sort(
        (a, b) => b[1] - a[1]
      );
      // Vaciar top de Madrid
      madridTop.querySelectorAll("div").forEach((div) => div.remove());
      // Actualizar top de Madrid
      for (let [host, count] of sortedMadridCount) {
        // Crear elementos HTML necesarios
        let div = document.createElement("div");
        let color = document.createElement("div");
        let p = document.createElement("p");
        let span = document.createElement("span");
        // Aplicar estilos
        color.style.background = hostColors[host];
        p.classList.add("host-count");
        p.textContent = hostNames[host];
        span.textContent = count;
        // Añadir elementos a la web
        p.appendChild(span);
        div.appendChild(color);
        div.appendChild(p);
        madridTop.appendChild(div);
      }

      // Ordenador contador de alojamientos de Barcelona
      let sortedBarcelonaCount = Object.entries(barcelonaCount).sort(
        (a, b) => b[1] - a[1]
      );
      // Vaciar top de Barcelona
      barcelonaTop.querySelectorAll("div").forEach((div) => div.remove());
      for (let [host, count] of sortedBarcelonaCount) {
        // Crear elementos HTML necesarios
        let div = document.createElement("div");
        let color = document.createElement("div");
        let p = document.createElement("p");
        let span = document.createElement("span");
        // Aplicar estilos
        color.style.background = hostColors[host];
        p.classList.add("host-count");
        p.textContent = hostNames[host];
        span.textContent = count;
        // Añadir elementos a la web
        p.appendChild(span);
        div.appendChild(color);
        div.appendChild(p);
        barcelonaTop.appendChild(div);
      }

      changingRadius = false;
    })
    .catch(() => (changingRadius = false));
}

// MAIN ------------------------------------------------------------------------------------

// Cambiar TMS por defecto
changeMapLayer("stamen-toner");

// Capa del mapa de tráfico
let categoryLayer = null;

// Variable para relaciones id-nombre
let hostNames = {};

// Variables para el contador de alojamientos de cada host
let madridCount = {};
let barcelonaCount = {};

// Variable para indicar que se está cambiando el radio
changingRadius = false;

// Variable para relaciones id-color
let hostColors = {};

// DOMs de los tops de cada ciudad
const madridTop = document.querySelector(".top-madrid-list");
const barcelonaTop = document.querySelector(".top-barcelona-list");

// DOMs del slider
const radiusSlider = document.getElementById("radiusSlider");
const radiusValue = document.getElementById("radiusValue");

// Primera inicialización del mapa
updateCategoryMap(radiusSlider.value);
radiusValue.innerHTML = radiusSlider.value;

// Detectar el cambio de radio
radiusSlider.addEventListener("change", () => {
  updateCategoryMap(radiusSlider.value);
});
radiusSlider.addEventListener("input", () => {
  radiusValue.textContent = radiusSlider.value;
});
