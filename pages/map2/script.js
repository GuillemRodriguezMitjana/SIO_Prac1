// Cambiar TMS por defecto
changeMapLayer("osm-buildings");

// Crear capas individuales para cada tipo de alojamiento
const entireHomeLayer = L.layerGroup();
const privateRoomLayer = L.layerGroup();
const sharedRoomLayer = L.layerGroup();
const hotelRoomLayer = L.layerGroup();

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
    fillOpacity: 0.6,
  });
}

// Variables para almacenar los datos de cada tipo
const entireHomeData = [];
const privateRoomData = [];
const sharedRoomData = [];
const hotelRoomData = [];

// Generar mapa de categorías
Promise.all([
  fetch("./data/madrid_roomtype.geojson").then((response) => response.json()),
  fetch("./data/barcelona_roomtype.geojson").then((response) =>
    response.json()
  ),
])
  .then((data) => {
    // Función para almacenar características en arrays según el tipo de alojamiento
    const storeFeatures = (features) => {
      features.forEach((feature) => {
        // Almacenar el feature en el array correspondiente
        switch (feature.properties.room_type) {
          case "Entire home/apt":
            entireHomeData.push(feature);
            break;
          case "Private room":
            privateRoomData.push(feature);
            break;
          case "Shared room":
            sharedRoomData.push(feature);
            break;
          case "Hotel room":
            hotelRoomData.push(feature);
            break;
          default:
        }
      });
    };

    // Almacenar datos de Madrid y Barcelona
    storeFeatures(data[0].features);
    storeFeatures(data[1].features);

    // Función para crear los marcadores y añadirlos a las capas
    const createMarkersForLayer = (dataArray, layer) => {
      dataArray.forEach((feature) => {
        // Crear marcador
        const marker = pointToLayer(feature, [
          feature.geometry.coordinates[1],
          feature.geometry.coordinates[0],
        ]);

        // Añadir marcador a la capa
        layer.addLayer(marker);

        // Cambiar icono en función del tipo de alojamiento
        let roomTypePopup = "";
        switch (feature.properties.room_type) {
          case "Entire home/apt":
            roomTypePopup = `<i class="fa-solid fa-house" style="color: rgb(69, 69, 252)"></i>`;
            break;
          case "Private room":
            roomTypePopup = `<i class="fa-solid fa-lock" style="color: orange"></i>`;
            break;
          case "Shared room":
            roomTypePopup = `<i class="fa-solid fa-lock-open" style="color: green"></i>`;
            break;
          case "Hotel room":
            roomTypePopup = `<i class="fa-solid fa-square-h" style="color: rgb(255, 66, 66)"></i>`;
            break;
          default:
        }

        // Pop-up al hacer click en el marcador
        marker.bindPopup(
          `
          <div class="listing-card">
            <div class="listing-header">
              <div class="listing-type">
                ${roomTypePopup}
              </div>
              <p class="listing-price"><span>${feature.properties.price} €</span> / noche</p>
            </div>
            <h3 class="listing-title">${feature.properties.name}</h3>
            <div class="listing-img-container">
              <img src="${feature.properties.picture}">
            </div>
            <p class="listing-description">${feature.properties.description}</p>
            <div class="listing-info">
              <div class="accommodates">
                <i class="fa-solid fa-users"></i>
                <p>${feature.properties.accommodates}</p>
              </div>
              <div class="rooms">
                <i class="fa-solid fa-bed"></i>
                <p>${feature.properties.bedrooms}</p>
              </div>
              <div class="baths">
                <i class="fa-solid fa-bath"></i>
                <p>${feature.properties.bathrooms}</p>
              </div>
            </div>
            <a href="${feature.properties.url}" target="_blank" style="text-decoration: none; color: #3498db;">
              Ver más detalles
            </a>
          </div>
          `
        );
      });
    };

    // Crear los marcadores para cada tipo de habitación
    createMarkersForLayer(entireHomeData, entireHomeLayer);
    createMarkersForLayer(privateRoomData, privateRoomLayer);
    createMarkersForLayer(sharedRoomData, sharedRoomLayer);
    createMarkersForLayer(hotelRoomData, hotelRoomLayer);

    // Añadir las capas al mapa
    entireHomeLayer.addTo(map);
    privateRoomLayer.addTo(map);
    sharedRoomLayer.addTo(map);
    hotelRoomLayer.addTo(map);
  })
  .catch();

// Función para cambiar la visibilidad de las capas de tipo de alojamiento
function changeLayerView(button, type) {
  // Ignorar si el mapa se está centrando
  if (moving) return;

  // Cambiar estilos
  button.classList.toggle("visible");

  // Seleccionar la capa correspondiente
  let layer = null;
  switch (type) {
    case "entire-home":
      layer = entireHomeLayer;
      break;
    case "private-room":
      layer = privateRoomLayer;
      break;
    case "shared-room":
      layer = sharedRoomLayer;
      break;
    case "hotel-room":
      layer = hotelRoomLayer;
      break;
    default:
  }

  // Cambiar la visibilidad de la capa si se ha encontrado
  if (layer !== null) toggleLayerView(layer);
}
