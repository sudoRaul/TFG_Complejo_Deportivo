<script setup>
import { ref } from 'vue'
import Swal from 'sweetalert2'
import router from "@/router";

// Cogemos el rol y el token para evitar que se pueda entrar en otras vistas
const sesion = sessionStorage.getItem("usuario") || localStorage.getItem("usuario");
const token = sessionStorage.getItem("token") || localStorage.getItem("token") || null;
const rol = sesion ? JSON.parse(sesion).rol : null;

// Redireccianamos al home si no es admin registrado
if (rol !== "admin" || !token) {
  router.push("/");
}

const newFacility = ref({
  nombre: '',
  categoria: '',
  descripcion: '',
  disponibilidad: '',
  foto: '',
})

async function submitForm() {
  // Validación de campos obligatorios
  if (!newFacility.value.nombre || !newFacility.value.categoria || !newFacility.value.descripcion || !newFacility.value.disponibilidad || !newFacility.value.foto) {
    Swal.fire({
      icon: 'error',
      title: 'All fields are required',
      text: 'Please, complete all fields before submitting.',
      confirmButtonText: 'Send',
    });
    return;
  }

  const form = {
    nombre: newFacility.value.nombre,
    categoria: newFacility.value.categoria,
    descripcion: newFacility.value.descripcion,
    disponibilidad: newFacility.value.disponibilidad,
    foto: newFacility.value.foto,
  }

  try {
    const response = await fetch('http://127.0.0.1:5000/instalaciones', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(form),
    })

    if (!response.ok) throw new Error('Network response was not ok');

    Swal.fire({
      title: 'Facility added',
      text: 'The facility has been successfully added.',
      icon: 'success',
      confirmButtonText: 'Okey',
    })

    newFacility.value = { nombre: '', categoria: '', descripcion: '', disponibilidad: '', foto: '' }

  } catch (error) {
    console.error('Error:', error)
    Swal.fire({
      title: 'Error',
      text: 'There was an error adding the facility. Please try again.',
      icon: 'error',
      confirmButtonText: 'Try Again',
    })
  }
}
</script>

<template>
  <div class="container mt-5">
    <div class="card shadow p-4 facility-card">
      <h2 class="mb-4 text-center">Add new facility</h2>
      <form @submit.prevent="submitForm" class="needs-validation" novalidate>
        <div class="mb-3">
          <label for="name" class="form-label">🏷️ Name</label>
          <input type="text" id="name" class="form-control rounded-pill" v-model="newFacility.nombre" required />
        </div>

        <div class="mb-3">
          <label for="category" class="form-label">📚 Categoty</label>
          <input type="text" id="category" class="form-control rounded-pill" v-model="newFacility.categoria" required />
        </div>

        <div class="mb-3">
          <label for="descripcion" class="form-label">📝 Description</label>
          <textarea id="descripcion" class="form-control rounded-4" v-model="newFacility.descripcion" rows="3"
            required></textarea>
        </div>

        <div class="mb-3">
          <label for="availability" class="form-label">✅ Disponibility</label>
          <select v-model="newFacility.disponibilidad" class="form-control rounded-pill" name="disponibilidad" id="disp"
            required>
            <option value="" disabled>Select disponibility</option>
            <option value="yes">Sí</option>
            <option value="no">No</option>
          </select>
        </div>

        <div class="mb-3">
          <label for="photo" class="form-label">🖼️ Photo (URL)</label>
          <input type="url" id="photo" class="form-control rounded-pill" v-model="newFacility.foto" required />
        </div>

        <div class="d-grid mt-4">
          <button type="submit" class="btn btn-success rounded-pill btn-lg">
            Add Facility
          </button>
        </div>
      </form>

      <div v-if="newFacility.foto" class="text-center mt-5">
        <h5>Preview photo</h5>
        <img :src="newFacility.foto" alt="Vista previa" class="img-thumbnail rounded shadow-sm mt-3"
          style="max-width: 300px;" />
      </div>
    </div>
  </div>
</template>



<style>
.facility-card {
  border-radius: 1.5rem;
  background: #ffffff;
  transition: background 0.3s;
}

h2 {
  font-weight: 700;
}

.form-label {
  font-weight: 500;
}

.form-control,
.form-control:focus {
  background: #f8f9fa;
  color: #212529;
  border: 1px solid #ced4da;
  transition: background 0.3s, color 0.3s;
}

.form-control:focus {
  box-shadow: 0 0 0 2px #28a74533;
}

textarea.form-control {
  resize: vertical;
}

.btn-success {
  background-color: #28a745;
  border: none;
}

.btn-success:hover {
  background-color: #218838;
}

/* Modo oscuro */
body.dark-mode {
  background-color: #18191a !important;
  color: #e4e6eb;
}

body.dark-mode .facility-card {
  background: #242526 !important;
  color: #e4e6eb;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.7);
}

body.dark-mode .form-label {
  color: #b0b3b8;
}

body.dark-mode .form-control,
body.dark-mode .form-control:focus,
body.dark-mode textarea.form-control {
  background-color: #3a3b3c !important;
  color: #e4e6eb !important;
  border: 1px solid #555 !important;
}

body.dark-mode .form-control:focus,
body.dark-mode textarea.form-control:focus {
  background-color: #484a4d !important;
  color: #fff !important;
  border-color: #1877f2 !important;
  box-shadow: 0 0 0 2px #1877f2;
}

body.dark-mode .btn-success {
  background-color: #1877f2 !important;
  border: none;
  color: #fff !important;
}

body.dark-mode .btn-success:hover {
  background-color: #0056b3 !important;
}

body.dark-mode .img-thumbnail {
  background: #18191a;
  border: 1px solid #444;
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