<script setup>
import { useRouter } from "vue-router";
import { ref, onMounted, watch } from "vue";
const router = useRouter();

const emit = defineEmits(["sesionCerrada"]);

const props = defineProps({
  title: String,
  usuarioAutenticado: Object,
});

const isDarkMode = ref(false);
const hasNotifications = ref(false);
const mensajes = ref([]);

async function fetchMensajes() {
  if (props.usuarioAutenticado?.rol === 'admin') {
    try {
      const res = await fetch('http://127.0.0.1:5000/contacto/');
      mensajes.value = await res.json();
    } catch (e) {
      mensajes.value = [];
    }
  } else {
    mensajes.value = [];
  }
}

onMounted(async () => {
  const dark = localStorage.getItem("darkMode") === "true";
  isDarkMode.value = dark;
  if (dark) document.body.classList.add("dark-mode");
  await fetchMensajes();
});

watch(() => props.usuarioAutenticado, async (nuevo) => {
  await fetchMensajes();
}, { immediate: false });

// Función para cerrar sesión
function cerrarSesion() {
  emit("sesionCerrada", null);
  sessionStorage.removeItem("usuario");
  sessionStorage.removeItem("token");
  localStorage.removeItem("usuario");
  localStorage.removeItem("token");
  router.push("/");
  window.location.reload();
}

// Mostrar/ocultar menú responsive
function toggleMenu() {
  const menu = document.getElementById("navbarNav");
  if (menu.classList.contains("show")) {
    menu.classList.remove("show");
  } else {
    menu.classList.add("show");
  }
}

function toggleDarkMode() {
  isDarkMode.value = !isDarkMode.value;
  localStorage.setItem("darkMode", isDarkMode.value);
  document.body.classList.toggle("dark-mode");
}
</script>

<template>
  <header class="bg-light text-black main">
    <nav class="navbar navbar-expand-xxl navbar-light">
      <div class="container-fluid d-flex justify-content-between align-items-center">
        <h1 class="navbar-brand mb-0" @click="router.push('/')">
          <img src="@/images/iconos/logo.png" class="me-1 mt-2" alt="Logotipo" width="110px" height="110px" />
          <span class="fw-200 fs-5 textWhite">{{ title }} </span>
        </h1>


        <button class="navbar-toggler" type="button" @click="toggleMenu">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse justify-content-center" id="navbarNav">
          <ul class="navbar-nav text-center flex-lg-row flex-column align-items-center justify-content-center">
            <li class="nav-item">
              <router-link to="/" class="nav-link btn btn-light fs-5 px-lg-4 px-2 py-lg-2 py-1 rounded-pill mx-lg-2 mx-1"
                active-class="active">Home</router-link>
            </li>
            <!-- Internal anchor navigation links (HomePage sections) -->
            <li class="nav-item" v-if="!usuarioAutenticado">
              <a class="nav-link btn btn-light fs-5 px-lg-4 px-2 py-lg-2 py-1 rounded-pill mx-lg-2 mx-1" href="#instalaciones">Meet us</a>
            </li>
            
            <li class="nav-item" v-if="!usuarioAutenticado">
              <a class="nav-link btn btn-light fs-5 px-lg-4 px-2 py-lg-2 py-1 rounded-pill mx-lg-2 mx-1" href="#findus">Find us</a>
            </li>
            <li class="nav-item" v-if="!usuarioAutenticado">
              <a class="nav-link btn btn-light fs-5 px-lg-4 px-2 py-lg-2 py-1 rounded-pill mx-lg-2 mx-1" href="#contactus">Contact us</a>
            </li>

            <!-- Zona de administrador -->
            <li v-if="usuarioAutenticado?.rol === 'admin'" class="nav-item dropdown custom-dropdown">
              <a class="nav-link dropdown-toggle fs-5 px-4 py-2 rounded-pill mx-2" href="#" id="adminDropdown"
                role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Administration
              </a>
              <ul class="dropdown-menu" aria-labelledby="adminDropdown">
                <li><router-link class="dropdown-item" to="/user-panel">Users' Administration</router-link></li>
                <li><router-link class="dropdown-item" to="/facilities">Facilities' Administration</router-link></li>
                <li><router-link class="dropdown-item" to="/create-facility">Create Facilities</router-link></li>
              </ul>
            </li>
            <li v-if="usuarioAutenticado?.rol === 'admin'" class="nav-item dropdown custom-dropdown">
              <a class="nav-link dropdown-toggle fs-5 px-4 py-2 rounded-pill mx-2" href="#" id="adminDropdown2"
                role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Users info
              </a>
              <ul class="dropdown-menu" aria-labelledby="adminDropdown2">
                <li><router-link class="dropdown-item" to="/assistants">View reservations</router-link></li>
                <li><router-link class="dropdown-item" to="/info-users">View users info</router-link></li>
              </ul>
            </li>

            <!-- Zona de usuario -->
            <li v-if="usuarioAutenticado?.rol === 'usuario'" class="nav-item dropdown custom-dropdown">
              <a class="nav-link dropdown-toggle fs-5 px-4 py-2 rounded-pill mx-2" href="#" id="reservaDropdown"
                role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Reservas
              </a>
              <ul class="dropdown-menu" aria-labelledby="reservaDropdown">
                <li><router-link class="dropdown-item" to="/facilities">Make a reservation</router-link></li>
                <li><router-link class="dropdown-item" to="/reserves">My reservations</router-link></li>
              </ul>
            </li>

            <li v-if="usuarioAutenticado?.rol != 'admin' && usuarioAutenticado" class="nav-item">
              <router-link to="/contact" class="nav-link btn btn-light fs-5 px-4 py-2 rounded-pill mx-2"
                active-class="active">Contact</router-link>
            </li>
            <li v-if="!usuarioAutenticado" class="nav-item">
              <router-link to="/login" class="nav-link btn btn-light fs-5 px-4 py-2 rounded-pill mx-2"
                active-class="active">Login</router-link>
            </li>

            <!-- Menú de cuenta del usuario autenticado -->
            <li v-if="usuarioAutenticado" class="nav-item dropdown custom-dropdown">
              <a class="nav-link dropdown-toggle fs-5 px-4 py-2 rounded-pill mx-2" href="#" id="cuentaDropdown"
                role="button" data-bs-toggle="dropdown" aria-expanded="false">
                My account
              </a>
              <ul class="dropdown-menu" aria-labelledby="cuentaDropdown">
                <li><router-link class="dropdown-item" to="/my-profile">My Profile</router-link></li>
                <li v-if="usuarioAutenticado?.rol == 'admin'">
                  <router-link class="dropdown-item d-flex align-items-center position-relative" to="/messages">
                    Notifications
                    <span v-if="mensajes.length > 0"
                      class="badge bg-danger rounded-circle position-absolute top-0 start-100 translate-middle"
                      style="font-size: 0.7rem; width: 20px; height: 20px; display: flex; align-items: center; justify-content: center;">
                      {{ mensajes.length }}
                    </span>
                  </router-link>
                </li>
                <li><router-link class="dropdown-item" to="/physical-analysis">Physical Analysis</router-link></li>
                <li>
                  <a @click.prevent="cerrarSesion"><router-link class="dropdown-item text-danger"
                      to="/">Logout</router-link></a>
                </li>
              </ul>
            </li>
          </ul>

          <!-- Bienvenida -->
          <div v-if="usuarioAutenticado" class="ms-5 d-block d-lg-block me-5">
            <h6 class="d-block text-center fs-5">
              Bienvenid@, {{ usuarioAutenticado?.nombre }}
            </h6>
          </div>
          <!-- Interruptor Modo Oscuro -->
          <div class="form-check form-switch d-block d-lg-block d-flex justify-content-center align-items-center gap-2 me-3">
            <input class="form-check-input" type="checkbox" role="switch" id="darkModeSwitch" :checked="isDarkMode"
              @change="toggleDarkMode" />
            <label class="form-check-label" for="darkModeSwitch">
              {{ isDarkMode ? '🌙' : '🌞' }}
            </label>
          </div>
        </div>
      </div>
    </nav>
  </header>
</template>


<style scoped>

/* Hover para dropdown */
.custom-dropdown:hover .dropdown-menu {
  display: block;
  margin-top: 0;
}

/* Estilo de los links en el navbar */
.navbar-nav .nav-item .nav-link {
  font-weight: 600;
  text-transform: uppercase;
  color: #333;
  padding: 0.5rem 1.5rem;
  transition: all 0.3s ease;
  border-radius: 30px;
  margin: 0 8px;
}


/* Efecto de hover en los links */
.navbar-nav .nav-item .nav-link:hover {
  background-color: #007bff;
  color: white;
  box-shadow: 0 4px 10px rgba(0, 123, 255, 0.2);
}

/* Estilo para el dropdown */
.custom-dropdown .dropdown-toggle {
  font-weight: 600;
  color: #007bff;
  background-color: transparent;
  padding: 0.5rem 1.5rem;
  border-radius: 30px;
  transition: all 0.3s ease;
}

.custom-dropdown .dropdown-toggle:hover {
  background-color: #f1f1f1;
  color: #0056b3;
}

/* Estilo para el menu del dropdown */
.custom-dropdown .dropdown-menu {
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  min-width: 200px;
}

/* Estilo para los items del dropdown */
.custom-dropdown .dropdown-item {
  padding: 10px 20px;
  font-weight: 500;
  color: #333;
  transition: background-color 0.3s ease;
}

.custom-dropdown .dropdown-item:hover {
  background-color: #007bff;
  color: white;
  cursor: pointer;
}

/* Estilo para el elemento activo */
.navbar-nav .nav-item .nav-link.active {
  background-color: #007bff;
  color: white;
  box-shadow: 0 4px 10px rgba(0, 123, 255, 0.3);
}

/* Estilo del navbar cuando se hace scroll */
.navbar {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

body.dark-mode nav {
  background-color: white;
  color: white !important;
}


body.dark-mode .nav-link {
  background-color: black;
  color: white !important;
}

body.dark-mode li {
  background-color: black !important;
  color: white !important;
}

body.dark-mode header,
body.dark-mode nav.navbar {
  background-color: black !important;
  /* fondo oscuro */
}



/* Activo en modo oscuro */

body.dark-mode .nav-link.active {
  background-color: #495057 !important;
  color: #ffffff !important;
  box-shadow: 0 4px 10px rgba(255, 255, 255, 0.1);
}

.body.dark-mode h1 {
  color: black;
}

.navbar-brand {
  color: #000 !important;
}

/* Centrar el interruptor de modo oscuro */
.form-check.form-switch {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  margin-left: 0 !important;
  gap: 0.5rem;
}
.form-check-input {
  width: 2.5em;
  height: 1.5em;
  margin-left: 0 !important;
}

body.dark-mode .textWhite {
  color: white;
}

body.dark-mode .dropdown-menu {
  background-color: #000 !important;
  border: 1px solid #222 !important;
  box-shadow: none !important;
}


body.dark-mode .dropdown-item {
  background-color: #000 !important;
  color: #fff !important;
}

body.dark-mode .dropdown-toggle {
  border: 0.01cm solid white;
}


body.dark-mode .dropdown-item:hover,
body.dark-mode .dropdown-item:focus {
  background-color: #007bff !important;
  color: #fff !important;
}

/* Estilo para el círculo de notificación */
.notification-dot {
  width: 10px;
  height: 10px;
  display: inline-block;
}

body.dark-mode  .navbar-toggler-icon{
  background-color: white !important;
}
body.dark-mode .navbar-toggler {
  border-color: white !important;
  color: white !important;
  background-color: white !important;
}
</style>
