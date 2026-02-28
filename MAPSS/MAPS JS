// Initialize the map
var map = L.map('map').setView([10.3157, 123.8854], 13);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Define a red icon
var redIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
  shadowUrl: 'https://unpkg.com/leaflet/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

// Example sensor locations
var sensorLocations = [
  { name: "Sensor 1", coords: [10.3157, 123.8854] },
  { name: "Sensor 2", coords: [10.3200, 123.9000] },
  { name: "Sensor 3", coords: [10.3100, 123.8800] }
];

// Add red pins for each sensor
sensorLocations.forEach(function(sensor) {
  L.marker(sensor.coords, { icon: redIcon })
    .addTo(map)
    .bindPopup("<b>" + sensor.name + "</b><br>Monitoring location");
});
