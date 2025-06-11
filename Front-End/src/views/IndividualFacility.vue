<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import Swal from 'sweetalert2'
import router from "@/router";


// Cogemos el rol y el token para evitar que se pueda entrar en otras vistas
const sesion = sessionStorage.getItem("usuario") || localStorage.getItem("usuario");
const token = sessionStorage.getItem("token") || localStorage.getItem("token") || null;
const rol = sesion ? JSON.parse(sesion).rol : null;

// Redireccianamos al home si no es admin registrado
if (!token) {
  router.push("/");
}

const route = useRoute()
const instalaciones = ref([])
const cargando = ref(true)
const error = ref(null)

const categoriaSeleccionada = computed(() => route.params.category)

async function obtenerInstalaciones() {
  try {
    cargando.value = true
    const response = await fetch(`http://127.0.0.1:5000/instalaciones?categoria=${categoriaSeleccionada.value}`)
    if (!response.ok) throw new Error('Reserves cannot be found')
    instalaciones.value = await response.json()
  } catch (err) {
    error.value = err.message
  } finally {
    cargando.value = false
  }
}

onMounted(obtenerInstalaciones)

async function actualizarRol(instalacionID, nuevaDisponibilidad) {
  try {
    const response = await fetch(`http://127.0.0.1:5000/instalaciones/${instalacionID}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ disponibilidad: nuevaDisponibilidad }),
    })

    if (!response.ok) throw new Error("Error updating availability")

    Swal.fire({
      icon: "success",
      title: "Availability updated",
      text: `The availability now is ${nuevaDisponibilidad}`,
      timer: 2000,
      showConfirmButton: false,
    })

    obtenerInstalaciones()
  } catch (err) {
    console.error(err.message)
  }
}

async function eliminarUsuario(instalacionID) {
  const confirmacion = await Swal.fire({
    title: "Are you sure?",
    text: "This action cannot be undone.",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#d33",
    cancelButtonColor: "#3085d6",
    confirmButtonText: "Yes, delete it!",
    cancelButtonText: "Cancel",
  })

  if (confirmacion.isConfirmed) {
    try {
      const response = await fetch(`http://127.0.0.1:5000/instalaciones/${instalacionID}`, {
        method: "DELETE",
      })

      if (!response.ok) throw new Error("Error deleting facility")

      Swal.fire({
        icon: "success",
        title: "Facility deleted",
        text: "The facility has been successfully deleted",
        timer: 2000,
        showConfirmButton: false,
      })

      obtenerInstalaciones()
    } catch (err) {
      console.error(err.message)
    }
  }
}

// ✅ Función para reservar instalación con validación de fecha y hora
async function reservarInstalacion(instalacionID) {
  const hoy = new Date().toISOString().split('T')[0];

  const { value: formValues } = await Swal.fire({
    title: 'Reserve facility',
    html: `
      <input type="date" id="fecha" class="swal2-input" min="${hoy}">
      <select id="hora" class="swal2-input">
        <option value="" disabled selected>Select the time</option>
        ${Array.from({ length: 14 }, (_, i) => {
      const hour = (i + 8).toString().padStart(2, '0');
      return `<option value="${hour}:00">${hour}:00</option>`;
    }).join("")}
      </select>
    `,
    focusConfirm: false,
    showCancelButton: true,
    preConfirm: () => {
      const fecha = document.getElementById('fecha').value;
      const hora = document.getElementById('hora').value;

      const ahora = new Date();
      const fechaHoraReserva = new Date(`${fecha}T${hora}`);

      // Validación de fecha: no puede ser anterior al día de hoy
      if (fecha < hoy) {
        Swal.showValidationMessage('The date cannot be in the past');
        return false;
      }

      // Validación de hora: no puede ser anterior a la hora actual
      if (fechaHoraReserva < ahora) {
        Swal.showValidationMessage('The time cannot be in the past');
        return false;
      }

      return { fecha, hora };
    }
  });

  if (formValues) {
    const usuarioID = sesion ? JSON.parse(sesion).id : null;
    try {
      const response = await fetch('http://127.0.0.1:5000/reservas/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          id_usuario: usuarioID,
          id_instalacion: instalacionID,
          fecha: formValues.fecha,
          hora: formValues.hora
        })
      });

      if (!response.ok) throw new Error('Error making reservation');

      Swal.fire({
        icon: 'success',
        title: 'Reserve done',
        text: 'Your reservation has been successfully made',
        timer: 2000,
        showConfirmButton: false
      });
    } catch (error) {
      console.error(error.message);
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'There was an error making the reservation. Please try again later.',
      });
    }
  }
}
</script>

<template>
  <div class="container mt-5">
    <h2 class="text-center mb-5">🔧 Facilities of category: {{ categoriaSeleccionada }}</h2>

    <div v-if="cargando" class="text-center">
      <p>Loading...</p>
    </div>
    <div v-if="error" class="alert alert-danger text-center">
      <p>{{ error }}</p>
    </div>

    <div v-if="instalaciones.length > 0" class="row justify-content-center">
      <div v-for="instalacion in instalaciones" :key="instalacion.id" class="col-12 col-md-6 col-lg-4 mb-4">
        <div class="card h-100 shadow rounded-4 border-0">
          <img :src="instalacion.foto" class="card-img-top" :alt="instalacion.nombre" />

          <div class="card-body d-flex flex-column justify-content-between">
            <div class="text-center mb-3">
              <h5 class="card-title fw-bold">{{ instalacion.nombre }}</h5>
              <p class="card-text">{{ instalacion.descripcion }}</p>
              <span class="badge" :class="instalacion.disponibilidad === 'yes' ? 'bg-success' : 'bg-danger'">
                {{ instalacion.disponibilidad === 'yes' ? 'Available' : 'Not available' }}
              </span>
            </div>

            <div class="d-flex justify-content-center flex-wrap gap-2 mt-3">
              <!-- Admin buttons -->
              <template v-if="rol === 'admin'">
                <button class="btn btn-warning btn-sm px-3"
                  @click="actualizarRol(instalacion.id, instalacion.disponibilidad === 'yes' ? 'no' : 'yes')">
                  Change Availability
                </button>

                <button class="btn btn-danger btn-sm px-3" @click="eliminarUsuario(instalacion.id)">
                  Delete
                </button>
              </template>

              <!-- Usuario button -->
              <template v-else-if="rol === 'usuario' && instalacion.disponibilidad === 'yes'">
                <button class="btn btn-success btn-sm px-3" @click="reservarInstalacion(instalacion.id)">
                  Reserve
                </button>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
    <NoData v-else mensaje="There isn't facilities to show" submensaje="Inspect this section later" />

  </div>
</template>


<style scoped>
.card-img-top {
  height: 200px;
  object-fit: cover;
  border-top-left-radius: 1rem;
  border-top-right-radius: 1rem;
}

.card {
  transition: transform 0.2s ease-in-out;
}

.card:hover {
  transform: scale(1.02);
}

body.dark-mode .swal2-popup {
  background: #fff !important;
  color: #222 !important;
}

body.dark-mode .swal2-title,
body.dark-mode .swal2-html-container,
body.dark-mode .swal2-content,
body.dark-mode .swal2-confirm,
body.dark-mode .swal2-cancel,
body.dark-mode .swal2-close {
  color: #222 !important;
}

body.dark-mode .swal2-icon {
  color: inherit !important;
}
</style>
