<script setup>
import { ref, onMounted } from 'vue';
import Swal from 'sweetalert2';
import NoData from '@/components/NoData.vue';
import router from "@/router";


// Datos
const groupedReservations = ref({});
const loading = ref(true); // Nueva bandera de carga

// Cogemos el rol y el token para evitar que se pueda entrar en otras vistas
const sesion = sessionStorage.getItem("usuario") || localStorage.getItem("usuario");
const token = sessionStorage.getItem("token") || localStorage.getItem("token") || null;
const rol = sesion ? JSON.parse(sesion).rol : null;

if (rol !== "admin" || !token) {
  router.push("/");
}

// Función para agrupar reservas por instalación
const groupReservationsByFacility = (reservations) => {
  const grouped = {};

  reservations.forEach(reservation => {
    const facilityId = reservation.instalacion.id;
    if (!grouped[facilityId]) {
      grouped[facilityId] = {
        instalacion: reservation.instalacion,
        users: []
      };
    }
    grouped[facilityId].users.push(reservation.usuario);
  });

  return grouped;
};

// Simular petición fetch
const fetchReservations = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/reservas/');
    const data = await response.json();

    groupedReservations.value = groupReservationsByFacility(data);
    
  } catch (error) {
    console.error('Error loading the reserves', error);
    Swal.fire('Error', 'Error loading the reserves', 'error');
  } finally {
    loading.value = false; // Se marca como cargado cuando finalice
  }
};

onMounted(() => {
  fetchReservations();
});
</script>

<template>
  <div class="container mt-5">
    <h2 class="mb-4 text-center">Reservas bt Facility</h2>

    <!-- Condición de carga -->
    <div v-if="loading" class="text-center">
      <div class="spinner-border text-success" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <!-- Mostrar los datos si existen -->
    <div v-else-if="Object.keys(groupedReservations).length > 0" class="row g-4">
      <div v-for="(facility, id) in groupedReservations" :key="id" class="col-md-6">
        <div class="card shadow-sm rounded-4 p-3 h-100">
          <div class="card-body">
            <h3 class="card-title text-success mb-3">{{ facility.instalacion.nombre }}</h3>
            <p class="text-muted mb-4">Categoría: {{ facility.instalacion.categoria }}</p>
            <img :src="facility.instalacion.foto" class="w-50 h-25 rounded mb-3" :alt="facility.instalacion.nombre" />

            <h5 class="mb-3">Users reserved:</h5>
            <ul class="list-group list-group-flush">
              <li v-for="(user, index) in facility.users" :key="index" class="list-group-item">
                <strong class="textBlack">{{ user.nombre }} {{ user.apellido }}</strong><br />
                <small>Email: {{ user.email }}</small><br />
                <small>Edad: {{ user.edad }} años</small>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Mostrar NoData si no hay datos -->
    <NoData v-else mensaje="There isn't reserves rigth now" submensaje="Please, inspect this section later" />
  </div>
</template>

<style scoped>
.card {
  transition: transform 0.3s;
}
.card:hover {
  transform: scale(1.02);
}
.list-group-item {
  background-color: #f9f9f9;
}
body.dark-mode .textBlack{
  color: black !important;
}
</style>
