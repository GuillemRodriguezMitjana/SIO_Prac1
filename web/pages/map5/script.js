// Cambiar TMS por defecto
changeMapLayer("stamen-toner");

// Capa del mapa de tráfico
let categoryLayer = null;

let hostNames = {};
const madridTop = document.querySelector(".top-madrid-list");
let madridCount = {};
const barcelonaTop = document.querySelector(".top-barcelona-list");
let barcelonaCount = {};

changingRadius = false;

let hostColors = {};

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
  if (hostColors[hostId]) return hostColors[hostId];

  // Generar un color aleatorio si el host aún no tiene uno asignado
  let newColor = getRandomColor();
  hostColors[hostId] = newColor;
  return newColor;
}

// Función para actualizar el mapa de categorías
function updateCategoryMap(radius = 5) {
  // Ignorar cambio en caso de que no haya terminado uno previo
  if (changingRadius) return;
  else changingRadius = true;

  // Limpiar la capa de categorías actual
  if (categoryLayer) map.removeLayer(categoryLayer);

  madridCount = {};
  barcelonaCount = {};

  // Cargar los archivos GeoJSON
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
            color: getColor(feature.properties.host_id),
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8,
          });
        },
        onEachFeature: (feature, layer) => {
          hostNames[feature.properties.host_id] = feature.properties.host_name;

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

          const verified =
            feature.properties.host_identity_verified == "t"
              ? "#FF385C"
              : "transparent";

          // Popup con información del host
          layer.bindPopup(
            `
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
            </div>
            `
          );
        },
      }).addTo(map);

      let sortedMadridCount = Object.entries(madridCount).sort(
        (a, b) => b[1] - a[1]
      );
      madridTop.querySelectorAll("div").forEach((div) => div.remove());
      for (let [host, count] of sortedMadridCount) {
        let div = document.createElement("div");
        let color = document.createElement("div");
        let p = document.createElement("p");
        let span = document.createElement("span");

        color.style.background = hostColors[host];
        p.classList.add("host-count");
        p.textContent = hostNames[host];
        span.textContent = count;

        p.appendChild(span);
        div.appendChild(color);
        div.appendChild(p);
        madridTop.appendChild(div);
      }

      let sortedBarcelonaCount = Object.entries(barcelonaCount).sort(
        (a, b) => b[1] - a[1]
      );
      barcelonaTop.querySelectorAll("div").forEach((div) => div.remove());
      for (let [host, count] of sortedBarcelonaCount) {
        let div = document.createElement("div");
        let color = document.createElement("div");
        let p = document.createElement("p");
        let span = document.createElement("span");

        color.style.background = hostColors[host];
        p.classList.add("host-count");
        p.textContent = hostNames[host];
        span.textContent = count;

        p.appendChild(span);
        div.appendChild(color);
        div.appendChild(p);
        barcelonaTop.appendChild(div);
      }

      changingRadius = false;
    })
    .catch(() => (changingRadius = false));
}

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
