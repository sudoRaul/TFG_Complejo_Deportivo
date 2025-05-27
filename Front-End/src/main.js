import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'leaflet/dist/leaflet.css';

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'

import BootstrapVue3 from 'bootstrap-vue-3'

// Inicializamos la app Vue
const app = createApp(App)

app.use(BootstrapVue3)
app.use(router)

// Verificamos el modo oscuro preferido desde el localStorage
const darkMode = localStorage.getItem('darkMode') === 'true';

if (darkMode) {
  document.body.classList.add('dark-mode');
}

app.mount('#app')
