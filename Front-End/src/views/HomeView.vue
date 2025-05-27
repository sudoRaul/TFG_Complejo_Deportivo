<script setup>
import SiteMap from '@/components/SiteMap.vue';
import Carrusel from '@/components/Carrusel.vue';
import TarjetaInformativa from '@/components/TarjetaInformativa.vue';
import FAQ from '@/components/FAQ.vue';
import { ref, onMounted } from 'vue';

const reservas = ref([]);

const sesion = JSON.parse(sessionStorage.getItem("usuario") || localStorage.getItem("usuario") || null);
const email = sesion ? sesion.email : null;

async function fetchReservations() {
  try {
    const response = await fetch(`http://127.0.0.1:5000/reservas/usuario?email=${email}`);
    const data = await response.json();
    reservas.value = data;
  } catch (error) {
    console.error('Error loading the reserves', error);
  }
}

onMounted(() => {
  if (email) {
    fetchReservations();
  }
});
</script>

<template>
  <div class="container-fluid px-0">
    <!-- Carrusel -->
    <Carrusel />

    <!-- Transición en el bloque de reservas -->
    <transition name="fade" @before-enter="beforeEnter" @enter="enter" @leave="leave">
      <div v-if="reservas.length > 0" class="alert alert-info text-center mt-4">
        <h3>You have pending reserves!</h3>
        <p>Check your reservations and don't miss out on your scheduled activities.</p>
        <router-link to="/reserves"><button class="btn btn-primary fs-5">My reserves</button></router-link>
      </div>
    </transition>

    <!-- Sección de apertura de nuevas instalaciones -->
    <div class="row d-flex justify-content-around align-items-center mt-5 mb-5 g-0">
      <div class="col-xl-5 col-lg-7 col-md-12 col-sm-12 col-xs-12 px-3 px-lg-5">
        <h2 class="fs-1 fw-bold text-left">
          <img src="@/images/iconos/iconAdvertencia.png" alt="Icono advertencia" class="img-fluid mb-2" />
          <b class="text-primary"> Upcoming</b> opening at our facilities!
        </h2>
        <p class="text-left fs-5 fw-800">
          Wednesday, June 4th, 2025, come and enjoy our new swimming pool:
        </p>
        <div class="text-left fs-5 fw-800">
          ✅ <b>Free access for all users on the first day.</b><br />
          ✅ <b>Changing rooms with showers and secure lockers.</b><br />
          ✅ <b>Relaxation area with sunbeds to unwind in the sun.</b><br />
          ✅ <b>Constant cleaning service to keep everything spotless.</b><br />
          ✅ <b>Qualified staff available to assist you at all times.</b><br />
        </div>
      </div>
      <div class="col-xl-6 col-lg-4 col-md-8 col-xs-12 col-sm-12 text-center">
        <img src="@/images/piscina.jpeg" alt="Imagen Piscina" class="img-fluid w-100 rounded" />
      </div>
    </div>

    <!-- Tarjetas informativas -->
    <div class="container mt-4" id="instalaciones"></div>
      <div class="row g-4">
        <div class="col-md-12 col-xl-4">
          <TarjetaInformativa
            titulo="+15 facilities"
            descripcion="We offer multiple sports spaces for all tastes."
            icono="src\images\iconos\iconMultiSport.png"
            colorFondo="bg-primary"
          />
        </div>

        <div class="col-md-12 col-xl-4">
          <TarjetaInformativa
            titulo="Be Part of the Action!"
            descripcion="Join the biggest sports community in the city and start your healthy habit towards!"
            icono="src\images\iconos\iconJoin.png"
            colorFondo="bg-success"
            textColor="text-white"
          />
        </div>

        <div class="col-md-12 col-xl-4">
          <TarjetaInformativa
            titulo="10,000 users"
            descripcion="More than 10,000 active athletes in our facilities."
            icono="src\images\iconos\iconPeople.png"
            colorFondo="bg-warning"
            textColor="text-white"
          />
        </div>
      </div>
    </div>

    <!-- Flexibilidad -->
    <div class="row d-flex justify-content-around align-items-center mt-5 mb-5 g-0">
      <div class="col-xl-5 col-lg-7 col-md-12 col-sm-12 col-xs-12 px-3 px-lg-5">
        <h2 class="fs-1 fw-bold text-left">
          <b class="text-warning">Flexibility</b> in all facilities
        </h2>
        <p class="text-left fs-5 fw-800">
          In our facilities, you don't have to worry about anything extra-sporting:
        </p>
        <div class="text-left fs-5 fw-800">
          ✅ <b>Changing rooms equipped with showers and sinks.</b><br />
          ✅ <b>Free cancellation of your reservation.</b><br />
          ✅ <b>Cleaning and maintenance service.</b><br />
          ✅ <b>Free parking for users.</b><br />
          ✅ <b>Security and surveillance service.</b><br />
          ✅ <b>Customer service support.</b><br />
        </div>
      </div>
      <div class="col-lg-5 col-md-8 col-xs-12 col-sm-12 text-left">
        <img src="@/images/campoFutbol.jpg" alt="" class="img-fluid w-100 rounded" />
      </div>
    </div>

    <!-- Más contenido -->
    <div class="row d-flex justify-content-around align-items-center mt-5 mb-5 g-0">
      <div class="col-lg-5 col-md-8 col-xs-12 col-sm-12 text-left">
        <img src="https://smashpadel4.com/smash/images/djimageslider/header/IMG_1474.JPG" alt="" class="img-fluid w-100 rounded" />
      </div>
      <div class="col-xl-5 col-lg-7 col-md-12 col-sm-12 col-xs-12 px-3 px-lg-5">
        <h2 class="fs-1 fw-bold text-left">
          <b class="text-warning">In company</b> everything is more fun
        </h2>
        <p class="text-left fs-5 fw-800">
          We manage your space so you can enjoy it to the fullest:
        </p>
        <div class="text-left fs-5 fw-800">
          ✅ <b>Come with your friends and enjoy a great day of sports.</b><br />
          ✅ <b>Book the facilities for private events.</b><br />
          ✅ <b>Meet more people with the same interests.</b><br />
          ✅ <b>We are your team to achieve your goals.</b><br />
          ✅ <b>Your place to train and a team to grow with.</b><br />
          ✅ <b>More than a sports complex, a big family.</b><br />
        </div>
      </div>
    </div>

    <!-- Encuentra tu lugar -->
    <div class="row d-flex justify-content-around align-items-center mt-5 mb-5 g-0">
      <div class="col-xl-5 col-lg-7 col-md-12 col-sm-12 col-xs-12 px-3 px-lg-5">
        <h2 class="fs-1 fw-bold text-left">
          <b class="text-warning">Find </b> your sports place
        </h2>
        <p class="text-left fs-5 fw-800">
          We're here to offer you the best sports space. We love welcoming you!
        </p>
        <p class="text-left fs-5">
          Visit us and experience training in a unique environment, with facilities designed for your comfort and needs.
          Our sports complex is located in an easily accessible area, close to key points in the city.
        </p>
        <a href="https://www.google.es/maps/@38.3215561,-2.9007907,3a,75y,230.9h,82.01t/data=!3m7!1e1!3m5!1slXup1yg22rHPdP34JwCEkQ!2e0!6shttps:%2F%2Fstreetviewpixels-pa.googleapis.com%2Fv1%2Fthumbnail%3Fcb_client%3Dmaps_sv.tactile%26w%3D900%26h%3D600%26pitch%3D7.986498155500499%26panoid%3DlXup1yg22rHPdP34JwCEkQ%26yaw%3D230.89749623524398!7i16384!8i8192?entry=ttu&g_ep=EgoyMDI1MDQyMy4wIKXMDSoASAFQAw%3D%3D"
          target="_blank">
          <button class="btn btn-warning fs-5">View on Google Maps</button>
        </a>
      </div>
      <div class="col-xl-6 col-lg-4 col-md-8 col-xs-12 col-sm-12 text-left" id="findus">
        <SiteMap />
      </div>
    </div>

    <br />
    <br />
    <FAQ id="contactus"/>
</template>

<style scoped>
/* Transiciones */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}

/* Botón Hover */
button {
  transition: transform 0.3s ease, background-color 0.3s ease;
}

button:hover {
  transform: translateY(-5px);
  background-color: #007bff;
}
body.dark-mode .alert-info {
  background-color: #444;
  color: white;
  border-color: #666;
}

body.dark-mode button:hover {
  background-color: #007bff;
}

body.dark-mode .alert-info h3 {
  color: #f1f1f1;
}

body.dark-mode .alert-info p {
  color: #ccc;
}
body.dark-mode h2 {
  color: #f1f1f1; /* Blanco suave para los títulos */
}

body.dark-mode p, 
body.dark-mode .fs-5, 
body.dark-mode .fs-1 {
  color: #ccc; /* Color de texto suave */
}

body.dark-mode .text-primary {
  color: #4f85b7; /* Mantén los colores de Bootstrap, pero más suaves */
}

body.dark-mode .text-warning {
  color: #ff9900; /* Color de advertencia ajustado */
}


body.dark-mode img {
  filter: brightness(0.8);
}


body.dark-mode img {
  border: 2px solid #444;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
}



body.dark-mode .TarjetaInformativa {
  background-color: #333; /* Fondo oscuro para las tarjetas */
  color: white;
  border-color: #444;
}

body.dark-mode .TarjetaInformativa .bg-primary {
  background-color: #5a6b8a; /* Ajuste de color para el fondo primario */
}

body.dark-mode .TarjetaInformativa .bg-success {
  background-color: #49746b; /* Fondo ajustado para éxito */
}

body.dark-mode .TarjetaInformativa .bg-warning {
  background-color: #7f6f3a; /* Fondo ajustado para advertencia */
}

html, body {
  max-width: 100vw;
  overflow-x: hidden;
}
</style>