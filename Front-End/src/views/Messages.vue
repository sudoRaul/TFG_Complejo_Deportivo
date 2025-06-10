<script setup>
import { ref, onMounted } from 'vue';
import Swal from 'sweetalert2';
import router from "@/router";


// Cogemos el rol y el token para evitar que se pueda entrar en otras vistas
const sesion = sessionStorage.getItem("usuario") || localStorage.getItem("usuario");
const token = sessionStorage.getItem("token") || localStorage.getItem("token") || null;
const rol = sesion ? JSON.parse(sesion).rol : null;

// Redireccianamos al home si no es admin registrado
if (rol !== "admin" || !token) {
  router.push("/");
}

// Estado para almacenar los contactos
const contactos = ref([]);
const loading = ref(true); // Nueva bandera de carga

// Cargar los contactos desde la API
const fetchContactos = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/contacto/');
    const data = await response.json();
    contactos.value = data;
  } catch (error) {
    console.error('Error loading contacts', error);
    //Swal.fire('Error', 'No se pudieron cargar los contactos', 'error');
  } finally {
    loading.value = false; // Se marca como cargado cuando finalice
  }
};

// Enviar la respuesta al contacto
const responderContacto = async (id, respuesta) => {
  if (!respuesta || respuesta.trim() === '') {
    Swal.fire('Error', 'The response cannot be empty', 'error');
    return;
  }

  try {
    const response = await fetch(`http://127.0.0.1:5000/contacto/${id}/responder`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ respuesta }),
    });

    if (!response.ok) {
      throw new Error('Error sending the response');
    }

    Swal.fire('Éxito', 'Response sent succesfully', 'success');

    // Opcional: limpiar el campo de respuesta
    const contacto = contactos.value.find(c => c.id === id);
    if (contacto) contacto.respuesta = '';
  } catch (error) {
    console.error('Error sending the response', error);
    Swal.fire('Error', 'Error sending the response', 'error');
  }
};

// Llamar a la función cuando el componente se monte
onMounted(() => {
  fetchContactos();
});
</script>

<template>
  <div v-if="contactos" class="container mt-5">
    <h2 class="mb-4 text-center">Contacts' Messages</h2>

    <!-- Condición de carga -->
    <div v-if="loading" class="text-center">
      <div class="spinner-border text-success" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div class="d-flex justify-content-around row">
      <div v-for="contacto in contactos" :key="contacto.id"
        class="list-group-item mb-3 p-4 shadow-sm rounded col-xl-5 col-lg-5 col-xs-12 col-md-12">
        <h5>{{ contacto.nombre }} ({{ contacto.email }})</h5>
        <p><strong>Phone number:</strong> {{ contacto.telefono }}</p>
        <p><strong>Message:</strong> {{ contacto.comentario }}</p>

        <!-- Formulario de respuesta -->
        <div class="mt-3">
          <textarea v-model="contacto.respuesta" class="form-control" rows="4"
            placeholder="Writing your answer..."></textarea>
          <button @click="responderContacto(contacto.id, contacto.respuesta)" class="btn btn-success mt-3"
            :disabled="!contacto.respuesta">
            Send Response
          </button>
        </div>
      </div>
    </div>
    
  </div>
  <NoData v-else mensaje="There isn't messages now" submensaje="Inspect this section later" />
</template>

<style scoped>
.list-group-item {
  background-color: #f9f9f9;
  border: 1px solid #ddd;
}

textarea {
  resize: none;
}

.btn-success {
  background-color: #10e141;
  border: none;
}

.btn-success:hover {
  background-color: #218838;
}

body.dark-mode {
  background-color: #18191a !important;
  color: #e4e6eb;
}

body.dark-mode .container {
  color: #e4e6eb;
}

body.dark-mode .list-group-item {
  background-color: #242526 !important;
  color: #e4e6eb !important;
  border: 1px solid #444 !important;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.7);
}

body.dark-mode textarea.form-control {
  background-color: #3a3b3c !important;
  color: #e4e6eb !important;
  border: 1px solid #555 !important;
}

body.dark-mode textarea.form-control:focus {
  background-color: #484a4d !important;
  color: #fff !important;
  border-color: #1877f2 !important;
  box-shadow: 0 0 0 2px #1877f2;
}

body.dark-mode .btn-success {
  background-color: #1877f2 !important;
  color: #fff !important;
  border: none;
}

body.dark-mode .btn-success:hover {
  background-color: #0056b3 !important;
}

body.dark-mode h2,
body.dark-mode p,
body.dark-mode strong {
  color: #e4e6eb !important;
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
