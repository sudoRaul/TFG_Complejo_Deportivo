<script setup>
import { onMounted } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

onMounted(() => {
  const mapId = 'map';
  const mapElement = document.getElementById(mapId);

  if (!mapElement) {
    console.warn(`Elemento no encontrado: ${mapId}`);
    return;
  }

  // Coordenadas válidas de Arroyo del Ojanco, Jaén
  const lat = 38.3215561;
  const lng = -2.9007907;

  const map = L.map(mapId).setView([lat, lng], 13);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
  }).addTo(map);

  L.marker([lat, lng])
    .addTo(map)
    .bindPopup('La Morada, Arroyo del Ojanco')
    .openPopup();
});
</script>

<template>
  <div
    id="map"
    class="map-container mb-5 shadow col-md-5 col-xl-5 col-sm-12 mt-4 text-center ms-2"
    style="height: 400px; width: 100%; border-radius: 10px; background-color: #f0f0f0;"
  ></div>
</template>
