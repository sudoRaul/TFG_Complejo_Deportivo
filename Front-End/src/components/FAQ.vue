
<script setup>
import { ref } from 'vue'


const items = ref([
  { title: 'How can I book a court at the sports center?', content: 'To make a reservation, you need to log in or register and access the reservation area to choose the desired facility.' },
  { title: 'What are the opening and closing hours of the sports center?', content: 'The sports center is open from 8:00 AM to 10:00 PM every day of the year.' },
  { title: 'Is it necessary to bring my own equipment?', content: 'Yes, all sports equipment must be brought by users, except in the gym.' },
  { title: 'What do I need for the gym?', content: 'To access the gym, it is mandatory to bring your own towel.' },
  { title: 'Are there changing rooms and showers?', content: 'Yes, all facilities have their own changing rooms and showers.' },
])

// Índice del acordeón actualmente abierto
const activeIndex = ref(null)

function toggleItem(index) {
  // Si ya está abierto, ciérralo
  activeIndex.value = activeIndex.value === index ? null : index
}
</script>

<template>
  <div class="container my-4">
    <div class="row justify-content-center align-items-center">
      <!-- Acordeón FAQ -->
      <div class="accordion accordion-flush col-12 col-md-6 mb-4 mb-md-0" id="accordionFlushExample">
        <h2 class="fw-bold">FAQ</h2>
        <br>
        <div class="accordion-item" v-for="(item, index) in items" :key="index">
          <h2 class="accordion-header" :id="'flush-heading' + index">
            <button class="accordion-button" :class="{ collapsed: activeIndex !== index }" type="button"
              @click="toggleItem(index)">
              <strong class="fs-5">{{ item.title }}</strong>
            </button>
          </h2>
          <div :id="'flush-collapse' + index" class="accordion-collapse collapse" :class="{ show: activeIndex === index }"
            :aria-labelledby="'flush-heading' + index">
            <div class="accordion-body fs-6">
              {{ item.content }}
            </div>
          </div>
        </div>
      </div>

      <!-- Contenedor de imagen y texto -->
      <div class="bg-light col-12 col-md-5 rounded-3 mt-3 mt-md-0">
        <div class="row ms-1 col-12">
          <img src="@/images/iconos/iconMessage.webp" class="col-2" alt="Icono mensaje">
          <p class="fs-4 fw-bolder col-8 mt-3">CAN`T FIND YOUR ANSWER?</p>
        </div>
        <br><br>
        <!-- Contenedor flex para centrar el botón -->
        <div class="d-flex justify-content-center">
          <router-link to="/contact" class="btn btn-primary col-10 col-md-6 mb-3 text-center">
            Contact Us
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Aseguramos que la columna de FAQ y la columna de contacto ocupen el 100% del ancho en pantallas pequeñas */
.accordion {
  max-width: 100%;
}

.bg-light {
  max-width: 100%;
}



body.dark-mode {
  background-color: #18191a !important;
  color: #e4e6eb;
}

body.dark-mode .accordion,
body.dark-mode .accordion-flush {
  background-color: transparent !important;
  color: #e4e6eb;
}

body.dark-mode .accordion-item {
  background-color: #242526 !important;
  border-color: #333 !important;
}

body.dark-mode .accordion-button {
  background-color: #3a3b3c !important;
  color: #e4e6eb !important;
  border: none;
}

body.dark-mode .accordion-button.collapsed {
  background-color: #242526 !important;
  color: #b0b3b8 !important;
}

body.dark-mode .accordion-button:focus {
  box-shadow: 0 0 0 2px #1877f2;
}

body.dark-mode .accordion-body {
  background-color: #242526 !important;
  color: #e4e6eb !important;
}

body.dark-mode .bg-light {
  background-color: #242526 !important;
  color: #e4e6eb !important;
  box-shadow: 0 2px 16px rgba(0,0,0,0.7);
}

body.dark-mode .btn-primary {
  background-color: #1877f2 !important;
  border-color: #1877f2 !important;
  color: #fff !important;
  transition: background 0.3s;
}

body.dark-mode .btn-primary:hover,
body.dark-mode .btn-primary:focus {
  background-color: #0056b3 !important;
  border-color: #0056b3 !important;
  color: #fff !important;
}

body.dark-mode .fw-bold,
body.dark-mode .fs-4,
body.dark-mode .fs-5 {
  color: #e4e6eb !important;
}
</style>
