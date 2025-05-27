<script setup>
import { ref } from 'vue';
import Swal from 'sweetalert2';
import router from "@/router";


// Cogemos el rol y el token para evitar que se pueda entrar en otras vistas
const sesion = sessionStorage.getItem("usuario") || localStorage.getItem("usuario");
const token = sessionStorage.getItem("token") || localStorage.getItem("token") || null;
const rol = sesion ? JSON.parse(sesion).rol : null;

// Redireccianamos al home si no es admin registrado
if (rol !== "usuario" || !token) {
  router.push("/");
}

// Definimos los datos del formulario
const form = ref({
    nombre: '',
    apellido: '',
    email: '',
    telefono: '',
    comentario: '',
});

// Función que se llama al enviar el formulario
const handleSubmit = async () => {
  // Validación simple
  if (!form.value.nombre || !form.value.apellido || !form.value.email || !form.value.telefono || !form.value.comentario) {
    Swal.fire({
      icon: 'error',
      title: 'Oops...',
      text: 'All fields are required.',
    });
    return;
  }

  try {
    // Hacemos la petición POST
    const response = await fetch('http://127.0.0.1:5000/contacto/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(form.value),
    });

    // Si la petición es exitosa, mostramos un mensaje de éxito
    Swal.fire({
      icon: 'success',
      title: 'Form sent',
      text: 'Thanks to contact us!',
    });

    // Limpiamos el formulario
    form.value = {
      nombre: '',
      apellido: '',
      email: '',
      telefono: '',
      comentario: '',
    };
  } catch (error) {
    // Si ocurre un error, mostramos un mensaje de error
    Swal.fire({
      icon: 'error',
      title: 'Something was wrong',
      text: 'The form could not be sent. Please try it later.',
    });
    console.error('Error sending the form:', error);
  }
};
</script>

<template>
    <div class="container mt-5">
        <div class="row">
            <!-- Columna de texto con íconos -->
            <div class="col-md-6">
                <h2 class="fw-bold fs-1">We want to hear you!</h2>
                <p class="text-muted">Put your message, suggestion o doubt and our team will respond you as possible.</p>
                <div class="d-flex flex-column">
                    <div class="d-flex align-items-center mb-3">
                        
                        <span class="fs-5">💪Consult any questions with our administrator.</span>
                    </div>
                    <div class="d-flex align-items-center mb-3">
                        <span class="fs-5">✍️Write to us what’s on your mind.</span>
                    </div>
                    <div class="d-flex align-items-center mb-3">
                        <span class="fs-5">📩Receive a quick response to your email.</span>
                    </div>
                    <div class="d-flex align-items-center mb-3">
                        <span class="fs-5">😉We’re here to help you.</span>
                    </div>
                </div>
            </div>

            <!-- Columna de formulario -->
            <div class="col-md-6">
                <form @submit.prevent="handleSubmit" class="bg-light p-4 rounded shadow-sm">
                    <div class="mb-3">
                        <label for="nombre" class="form-label">Name</label>
                        <input type="text" id="nombre" class="form-control" v-model="form.nombre"
                            placeholder="Introduce your name" required />
                    </div>

                    <div class="mb-3">
                        <label for="apellido" class="form-label">Surname</label>
                        <input type="text" id="apellido" class="form-control" v-model="form.apellido"
                            placeholder="Introduce your surname" required />
                    </div>

                    <div class="mb-3">
                        <label for="email" class="form-label">E-mail</label>
                        <input type="email" id="email" class="form-control" v-model="form.email"
                            placeholder="Introduce your email" required />
                    </div>

                    <div class="mb-3">
                        <label for="telefono" class="form-label">Phone Number</label>
                        <input type="tel" id="telefono" class="form-control" v-model="form.telefono"
                            placeholder="Introduce your telephone number" required />
                    </div>

                    <div class="mb-3">
                        <label for="comentario" class="form-label">Comment</label>
                        <textarea id="comentario" class="form-control" v-model="form.comentario"
                            placeholder="Write your message" required></textarea>
                    </div>

                    <button type="submit" class="btn btn-primary w-100 mt-3">Submit</button>
                </form>
            </div>
        </div>
    </div>
</template>



<style scoped>
.bg-light {
    background-color: #f8f9fa !important;
}

button.btn-primary {
    transition: background-color 0.3s ease;
}

button.btn-primary:hover {
    background-color: #0056b3;
    border-color: #0056b3;
}

button.btn-primary:focus {
    box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

body.dark-mode {
    background-color: #18191a !important;
    color: #e4e6eb;
}

body.dark-mode .container {
    background: transparent;
    color: #e4e6eb;
}

body.dark-mode .bg-light {
    background-color: #242526 !important;
    color: #e4e6eb;
    box-shadow: 0 2px 16px rgba(0,0,0,0.6);
}

body.dark-mode .form-label {
    color: #b0b3b8;
}

body.dark-mode .form-control {
    background-color: #737374;
    color: #e4e6eb;
    border: 1px solid #555;
}

body.dark-mode .form-control:focus {
    background-color: #737374;
    color: #fff;
    border-color: #1877f2;
    box-shadow: 0 0 0 2px #1877f2;
}

body.dark-mode textarea.form-control {
    background-color: #555;
    color: #e4e6eb;
}

body.dark-mode .btn-primary {
    background-color: #1877f2;
    border-color: #1877f2;
    color: #fff;
    transition: background 0.3s;
}

body.dark-mode .btn-primary:hover,
body.dark-mode .btn-primary:focus {
    background-color: #0056b3;
    border-color: #0056b3;
    color: #fff;
}

body.dark-mode .shadow-sm {
    box-shadow: 0 2px 16px rgba(0,0,0,0.8) !important;
}

body.dark-mode .fw-bold,
body.dark-mode .fs-1,
body.dark-mode .fs-5,
body.dark-mode .text-muted {
    color: #e4e6eb !important;
}

body.dark-mode textarea::placeholder{
    color: white;
}
</style>