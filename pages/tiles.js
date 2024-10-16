// Definir TMSs
const openstreetmapsLayer = L.tileLayer(
  "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
  {
    minZoom: 2,
    maxZoom: 20,
  }
);
const stamenTonerLayer = L.tileLayer(
  "https://tiles.stadiamaps.com/tiles/stamen_toner/{z}/{x}/{y}{r}.png",
  {
    minZoom: 2,
    maxZoom: 20,
  }
);
const StadiaAlidadeSatelliteLayer = L.tileLayer(
  "https://tiles.stadiamaps.com/tiles/alidade_satellite/{z}/{x}/{y}{r}.jpg",
  {
    minZoom: 2,
    maxZoom: 20,
  }
);
const OpenTopoMapLayer = L.tileLayer(
  "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
  {
    minZoom: 2,
    maxZoom: 20,
  }
);
const EsriWorldImageryLayer = L.tileLayer(
  "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
  {
    minZoom: 2,
    maxZoom: 20,
  }
);
const OsmBuildingsLayer = L.tileLayer(
  "https://tile-a.openstreetmap.fr/hot/{z}/{x}/{y}.png",
  {
    minZoom: 2,
    maxZoom: 20,
  }
);
let OsmBuildings;
layers = [
  openstreetmapsLayer,
  stamenTonerLayer,
  StadiaAlidadeSatelliteLayer,
  OpenTopoMapLayer,
  EsriWorldImageryLayer,
  OsmBuildingsLayer,
];

// Inicializar el mapa centrado en España
const map = L.map("map").setView([40.4168, -3.7038], 6);

// Variable para controlar si el mapa se está centrando
let moving = false;

// Añadir TMS por defecto
currentLayer = StadiaAlidadeSatelliteLayer;
currentLayer.addTo(map);
document.getElementById("alidade-satellite").classList.add("tms-selected");

// Detectar cambio de TMS
document.addEventListener("DOMContentLoaded", function () {
  const tmsItems = document.querySelectorAll(".tms-list li");

  tmsItems.forEach((item) => {
    item.addEventListener("click", function () {
      // Si se ha clickado a la TMS que ya está cargada, se ignora
      if (item.classList.contains("tms-selected")) return;
      tmsItems.forEach((i) => {
        if (i != this) i.classList.remove("tms-selected");
        else i.classList.add("tms-selected");
      });
      const selectedLayer = this.getAttribute("id");
      changeMapLayer(selectedLayer);
    });
  });
});

// Función para cambiar el mapa según la capa seleccionada
function changeMapLayer(layer) {
  let layersToKeep = [];

  if (layer !== "osm-buildings" && OsmBuildings) {
    // Si se quita la de OSM, se quitan también los edificios 3D
    map.removeLayer(OsmBuildings);
  } else if (layer == "osm-buildings") {
    // Si se pone la de OSM, primero guardamos todas las capas que no sean el TLS
    map.eachLayer(function (layer) {
      if (layer !== currentLayer) {
        layersToKeep.push(layer);
      }
    });
    // Luego las eliminamos
    map.eachLayer(function (layer) {
      if (layer !== currentLayer) {
        map.removeLayer(layer);
      }
    });
  }

  // Eliminamos la capa TLS
  map.removeLayer(currentLayer);
  // Ponemos la TLS a la que se ha cambiado
  switch (layer) {
    case "openstreetmaps":
      currentLayer = openstreetmapsLayer;
      break;
    case "stamen-toner":
      currentLayer = stamenTonerLayer;
      break;
    case "alidade-satellite":
      currentLayer = StadiaAlidadeSatelliteLayer;
      break;
    case "opentopomap":
      currentLayer = OpenTopoMapLayer;
      break;
    case "worldimagery":
      currentLayer = EsriWorldImageryLayer;
      break;
    case "osm-buildings":
      currentLayer = OsmBuildingsLayer;
      OsmBuildings = new OSMBuildings(map);
      OsmBuildings.load(
        "https://{s}.data.osmbuildings.org/0.2/59fcc2e8/tile/{z}/{x}/{y}.json"
      );
      break;
    default:
  }
  map.addLayer(currentLayer);

  // Recuperamos la resta de capas guardadas al principio
  layersToKeep.forEach((layer) => {
    map.addLayer(layer);
  });
}

// Función para centrar el mapa en unas coordenadas específicas
function centerMap(latitude, longitude, zoom) {
  const layersToHide = [];

  // Si ya está en la posición a la que se quiere ir, se ignora
  let currentCenter = map.getCenter();
  let currentZoom = map.getZoom();
  if (
    currentCenter.lat == latitude &&
    currentCenter.lng == longitude &&
    currentZoom == zoom
  ) {
    return;
  }

  // Se indica que el mapa está en movimiento
  moving = true;

  // Guardamos y eliminamos todas las capas que no sean TLS
  map.eachLayer(function (layer) {
    if (!layers.includes(layer)) {
      layersToHide.push(layer);
      map.removeLayer(layer);
    }
  });

  // Desplazamos el mapa con una velocidad en función de la distancia
  const distance = map.distance(currentCenter, L.latLng(latitude, longitude));
  let duration = Math.max(distance / 500000, 2);
  map.flyTo([latitude, longitude], zoom, { duration: duration });

  // Una vez terminado el desplazamiento, recuperamos las capas eliminadas, actualizamos la vista y avisamos que el desplazamiento ha terminado
  map.on("zoomend", function () {
    layersToHide.forEach(function (layer) {
      map.addLayer(layer);
    });
    currentCenter = map.getCenter();
    currentZoom = map.getZoom();
    map.setView([currentCenter.lat, currentCenter.lng], currentZoom);
    moving = false;
  });
}

// Función para centrar el mapa en una posición personalizada
document
  .getElementById("customPosForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    // Obtenemos los valores del formulario (latitud, longitud y zoom)
    const latitude = parseFloat(document.getElementById("latitude").value);
    const longitude = parseFloat(document.getElementById("longitude").value);
    const zoom = document.getElementById("zoom")
      ? document.getElementById("zoom").value
      : map.getZoom();

    // Si los valores son correctos, desplazamos el mapa
    if (!isNaN(latitude) && !isNaN(longitude)) {
      centerMap(latitude, longitude, zoom);
    }

    // Limpiamos los inputs del formulario
    document.getElementById("zoom").value = "";
    document.getElementById("latitude").value = "";
    document.getElementById("longitude").value = "";
  });

let hiddenLayers = [];

// Función para añadir o eliminar una capa
function toggleLayerView(layer) {
  if (hiddenLayers.includes(layer)) {
    map.addLayer(layer);
    hiddenLayers = hiddenLayers.filter((item) => item !== layer);
  } else {
    map.removeLayer(layer);
    hiddenLayers.push(layer);
  }
}
