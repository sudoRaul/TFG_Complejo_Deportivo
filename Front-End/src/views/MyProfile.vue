<script setup>
import { ref, onMounted } from 'vue';
import Swal from 'sweetalert2';
import router from "@/router";


const sesion = sessionStorage.getItem("usuario") || localStorage.getItem("usuario");
const rol = sesion ? JSON.parse(sesion).rol : null;
const id = sesion ? JSON.parse(sesion).id : null;
const token = sessionStorage.getItem("token") || localStorage.getItem("token") || null;

// Redireccianamos al home si no tiene un token registrado
if (!token) {
  router.push("/");
}

// Variables reactivas para el formulario
const form = ref({
    nombre: '',
    apellido: '',
    edad: '',
    email: '',
    sexo: '',
    peso: '',
    altura: '',
    telefono: '',
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
});

// Función para cargar los datos del usuario
const cargarDatosUsuario = async () => {
    try {
        if (!id) {
            router.push("/");
            return;
        }
        const response = await fetch(`http://127.0.0.1:5000/usuarios/${id}`);
        if (!response.ok) throw new Error('Error obtaining the user data.');
        const user = await response.json();
        form.value.nombre = user.nombre;
        form.value.apellido = user.apellido;
        form.value.edad = user.edad;
        form.value.email = user.email;
        form.value.sexo = user.sexo;
        form.value.peso = user.peso;
        form.value.altura = user.altura
        form.value.telefono = user.telefono
    } catch (error) {
        /*Swal.fire({
            icon: 'error',
            title: 'Error',
            text: error.message || 'No se pudo cargar la información del usuario.'
        });*/
        console.error("Error loading user data:", error);
    }
};

// Guardar campo individual al perder el foco
async function guardarCampo(campo) {
    try {
        if (!id) return;
        const updatedUser = { [campo]: form.value[campo] };
        const response = await fetch(`http://127.0.0.1:5000/usuarios/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updatedUser)
        });
        if (!response.ok) throw new Error('Error updating the profile.');
        Swal.fire({
            icon: 'success',
            title: 'Datas updated',
            text: 'The data has been updated successfully.'
        });
    } catch (error) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: error.message || 'There was a problem updating the profile.'
        });
    }
}



async function deleteAccount() {
    const result = await Swal.fire({
        title: 'Are you sure?',
        text: "You can't revert this action!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete account'
    })
    if (result.isConfirmed) {
        const response = await fetch(`http://127.0.0.1:5000/usuarios/${id}`, {
            method: 'DELETE',
        });
        if (response.ok) {
            localStorage.clear();
            sessionStorage.clear();
            location.href = '/';
        } else {
            Swal.fire(
                'Error',
                'It was not possible to delete the account now. Try later.',
                'error'
            );
        }
    }
}

onMounted(async () => {
    await cargarDatosUsuario();
});
</script>

<template>
    <div class="container mt-5">
        <div class="row align-content-center">

            <div class="col-md-6 col-lg-4 d-flex justify-content-center h-50 izqContainer">
                <!-- Contenedor Izquierdo: Avatar y Datos del Usuario -->
                <div class="user-info text-center">
                    <!-- Avatar -->
                    <div v-if="form.sexo == 'Male'" class="avatar mb-3">
                        <img src="@/images/avatar.png" alt="Avatar" class="img-fluid rounded-circle" />
                    </div>
                    <div v-else-if="form.sexo == 'Female'" class="avatar mb-3">
                        <img src="@/images/avatarFemenino.png" alt="Avatar" class="img-fluid rounded-circle" />
                    </div>
                    <div v-else class="avatar mb-3">
                        <img src="@/images/default-icon.png" alt="Avatar" class="img-fluid rounded-circle" />
                    </div>

                    <!-- Nombre y Rol -->
                    <h4 class="user-name" id="name">{{ form.nombre }} {{ form.apellido }}</h4>
                    <p class="user-role text-muted">{{ rol }}</p>
                    <button type="button" id="delete" @click="deleteAccount" class="btn btn-outline-danger col-12">Delete
                        Account</button>
                </div>
            </div>

            <div class="col-md-6 col-lg-8">
                <!-- Contenedor Derecho: Formulario con Estilo Minimalista -->
                <div class="p-4">
                    <h2 class="text-left mb-4">My Account</h2>
                    <h4 class="text-left mb-4" id="viewInfo">View and edit your personal info</h4>

                    <!-- Formulario -->
                    <form>
                        <div class="row">
                            <div class="mb-4 col-xl-6 col-lg-6 col-md-12 col-sm-12 col-xs-12">
                                <label for="name" class="form-label fs-4">Name</label>
                                <input type="text" v-model="form.nombre" id="name" class="form-control no-border fs-5"
                                    required @blur="guardarCampo('nombre')" />
                            </div>

                            <div class="mb-4 col-xl-6 col-lg-6 col-md-12 col-sm-12 col-xs-12">
                                <label for="lastname" class="form-label fs-4">Surname</label>
                                <input type="text" v-model="form.apellido" id="lastname"
                                    class="form-control no-border fs-5" required @blur="guardarCampo('apellido')" />
                            </div>

                            <div class="mb-4 col-xl-6 col-lg-6 col-md-12 col-sm-12 col-xs-12">
                                <label for="age" class="form-label fs-4">Age</label>
                                <input type="number" v-model="form.edad" id="age" class="form-control no-border fs-5"
                                    required @blur="guardarCampo('edad')" />
                            </div>

                            <div class="mb-4 col-xl-6 col-lg-6 col-md-12 col-sm-12 col-xs-12">
                                <label for="peso" class="form-label fs-4">Weight</label>
                                <input type="number" v-model="form.peso" id="peso" class="form-control no-border fs-5"
                                    required @blur="guardarCampo('peso')" />
                            </div>

                            <div class="mb-4 col-xl-6 col-lg-6 col-md-12 col-sm-12 col-xs-12">
                                <label for="altura" class="form-label fs-4">Height</label>
                                <input type="number" v-model="form.altura" id="altura"
                                    class="form-control no-border fs-5" required @blur="guardarCampo('altura')" />
                            </div>

                            <div class="mb-4 col-xl-6 col-lg-6 col-md-12 col-sm-12 col-xs-12">
                                <label for="sex" class="form-label fs-4">Sex</label>
                                <label id="sex" class="form-control no-border fs-5">{{ form.sexo }}</label>
                            </div>

                            <div class="mb-4 col-xl-6 col-lg-6 col-md-12 col-sm-12 col-xs-12">
                                <label for="phone" class="form-label fs-4">TPhone Number</label>
                                <label id="phone" class="form-control no-border fs-5">{{ form.telefono }}</label>
                            </div>

                            <div class="mb-4 col-xl-6 col-lg-6 col-md-12 col-sm-12 col-xs-12">
                                <label for="email" class="form-label fs-4">Email</label>
                                <label id="email" class="form-control no-border fs-5">{{ form.email }}</label>
                            </div>
                        </div>

                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.user-info {
    max-width: 200px;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}

.avatar {
    width: 150px;
    height: 150px;
    margin: 0 auto;
}

.avatar img {
    width: 100%;
    height: auto;
    border-radius: 50%;
}

.user-name {
    font-size: 1.25rem;
    font-weight: bold;
    margin-top: 10px;
}

.user-role {
    font-size: 1rem;
    color: #777;
}

h2,
h4 {
    color: #333;
    font-family: cursive;
}

.form-label {
    font-weight: bold;
}

.no-border {
    border: none;
    border-bottom: 2px solid transparent;
    border-radius: 0;
    padding-left: 0;
    padding-right: 0;
    padding-bottom: 5px;
}

.no-border:focus {
    outline: none;
    border-color: #007bff;
}



.izqContainer {
    background-color: rgb(243, 193, 188);
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

label,
input {
    font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
}

body.dark-mode #delete {
    background-color: rgb(238, 29, 29) !important;
    color: white !important;
}
body.dark-mode #delete:hover {
    background-color: rgb(255, 0, 0) !important;
    scale: 1.05;
    transition: background-color 0.2s, scale 0.5s;
}

body.dark-mode #viewInfo{
    color: #e4e6eb;
}

body.dark-mode #name{
    color: #e4e6eb;
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
