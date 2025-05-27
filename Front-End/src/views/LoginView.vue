<script setup>
import { ref, watch } from "vue";
import { useRouter } from "vue-router";
import Swal from 'sweetalert2';


const emit = defineEmits(["login-exitoso"]);

const isLogin = ref(true);
const router = useRouter();
const rememberMe = ref(false);

const form = ref({
  nombre: '',
  apellido: '',
  edad: '',
  altura: '',
  peso: '',
  sexo: '',
  telefono: '',
  email: '',
  contraseña: '',
  confPass: ''
});

const errorMessage = ref("");

// Limpiar el mensaje de error automáticamente después de 5 segundos
watch(errorMessage, (val) => {
  if (val) {
    setTimeout(() => {
      errorMessage.value = "";
    }, 10000);
  }
});

// Validación de contraseña
function validatePassword(password) {
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$/;
  return passwordRegex.test(password.trim());
}

async function enviarFormulario() {
  errorMessage.value = "";

  if (!isLogin.value) {
    if (form.value.contraseña !== form.value.confPass) {
      errorMessage.value = "Passwords do not match.";
      return;
    }

    if (form.value.sexo !== "Male" && form.value.sexo !== "Female") {
      errorMessage.value = "The field 'Sex' only accepts 'Male' or 'Female'.";
      return;
    }

    if (form.value.edad < 1 || form.value.edad > 120) {
      errorMessage.value = "You must be at least 1 year old and no more than 120.";
      return;
    }

    if (!validatePassword(form.value.contraseña)) {
      errorMessage.value = "Password must be at least 6 characters long, include one uppercase letter, one lowercase letter, one number, and one special character.";
      return;
    }
  }

  try {
    const endpoint = isLogin.value ? "/auth/login" : "/usuarios/";
    const payload = isLogin.value
      ? {
        email: form.value.email,
        password: form.value.contraseña,
      }
      : {
        nombre: form.value.nombre,
        apellido: form.value.apellido,
        email: form.value.email,
        contraseña: form.value.contraseña,
        edad: form.value.edad,
        rol: "usuario",
        altura: form.value.altura,
        peso: form.value.peso,
        sexo: form.value.sexo,
        telefono: form.value.telefono,
      };

    const response = await fetch("http://127.0.0.1:5000" + endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok) {
      errorMessage.value = data.message || "Something went wrong.";
      return;
    }


    // Login o registro exitoso
    const usuario = {
      id: data.usuario.id,
      nombre: data.usuario.nombre,
      email: data.usuario.email,
      edad: data.usuario.edad,
      rol: data.usuario.rol,
    };

    const storage = rememberMe.value ? localStorage : sessionStorage;
    storage.setItem("token", data.access_token);
    storage.setItem("usuario", JSON.stringify(usuario));

    emit("login-exitoso", usuario);
    router.push("/");

  } catch (error) {
    errorMessage.value = error.message || "Connection error.";
  }
}

async function sendEmailForgot() {
  const { value: email } = await Swal.fire({
    title: 'Recover password',
    input: 'email',
    inputLabel: 'Enter your email address',
    inputPlaceholder: 'your@email.com',
    confirmButtonText: 'Send',
    showCancelButton: true,
    inputValidator: (value) => {
      if (!value) {
        return 'You must enter your email!';
      }
      // Simple email validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(value)) {
        return 'Please enter a valid email address.';
      }
      return null;
    }
  });
  if (email) {
    try {
      const response = await fetch('http://127.0.0.1:5000/usuarios/recPassword', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      });
      const data = await response.json();
      if (!response.ok) {
        await Swal.fire('Error', data.error || 'An error occurred.', 'error');
        return;
      } else {
        await Swal.fire('Success', data.message || 'Recovery email sent! Check your inbox.', 'success');
      }
    } catch (e) {
      await Swal.fire('Error', 'Connection error. Please try again later.', 'error');
    }
  }
}

function toggleFormulario() {
  isLogin.value = !isLogin.value;
  form.value = {
    nombre: '',
    apellido: '',
    edad: '',
    altura: '',
    peso: '',
    sexo: '',
    telefono: '',
    email: '',
    contraseña: '',
    confPass: ''
  };
  rememberMe.value = false;
  errorMessage.value = "";
}
</script>


<template>
  <section class="min-vh-100 d-flex align-items-center justify-content-center">
    <div class="container" style="max-width: 850px;">
      <transition name="slide-fade" mode="out-in">
        <div class="card shadow" style="border-radius: 1rem;" :key="isLogin">
          <div class="row g-0 flex-md-row" :class="!isLogin ? 'flex-md-row-reverse' : ''">

            <!-- Imagen -->
            <div class="col-md-6 d-none d-md-block">
              <img src="https://entrenadorpersonaloriol.com/wp-content/uploads/2022/02/sports-tools.jpg"
                alt="form image" class="img-fluid h-100"
                :style="isLogin ? 'border-radius: 1rem 0 0 1rem; object-fit: cover;' : 'border-radius: 0 1rem 1rem 0; object-fit: cover;'" />
            </div>

            <!-- Formulario -->
            <div class="col-md-6 d-flex align-items-center">
              <div class="card-body p-4 p-lg-5 text-black w-100" style="max-height: 80vh; overflow-y: auto;">

                <form @submit.prevent="enviarFormulario">
                  <div class="d-flex align-items-center mb-2 pb-1">
                    <i class="fas fa-cubes fa-2x me-3" style="color: #ff6219;"></i>
                    <span class="h1 fw-bold mb-0">La Morada</span>
                  </div>

                  <h5 class="fw-normal mb-2 pb-2" style="letter-spacing: 1px;">
                    {{ isLogin ? 'Sign into your account' : 'Create a new account' }}
                  </h5>

                  <!-- Campos de registro -->
                  <div v-if="!isLogin">
                    <div class="form-outline mb-3">
                      <label class="form-label" for="nombre">Name
                        <input v-model="form.nombre" type="text" id="nombre" class="form-control form-control-lg"
                          required />
                      </label>
                    </div>
                    <div class="form-outline mb-3">
                      <label class="form-label" for="apellidos">Surname
                        <input v-model="form.apellido" type="text" id="apellidos" class="form-control form-control-lg"
                          required />
                      </label>
                    </div>
                    <div class="form-outline mb-3">
                      <label class="form-label" for="edad">Age
                        <input v-model="form.edad" type="number" id="edad" class="form-control form-control-lg"
                          required />
                      </label>
                    </div>
                    <div class="form-outline mb-3">
                      <label class="form-label" for="heigth">Height in centimetres
                        <input v-model="form.altura" type="number" id="heigth" class="form-control form-control-lg"
                          required />
                      </label>
                    </div>
                    <div class="form-outline mb-3">
                      <label class="form-label" for="weigth">Weight in kilograms
                        <input v-model="form.peso" type="number" id="weigth" class="form-control form-control-lg"
                          required />
                      </label>
                    </div>
                    <div class="form-outline mb-3">
                      <label class="form-label" for="numTel">Telephone number
                        <input v-model="form.telefono" type="number" id="numTel" class="form-control form-control-lg"
                          required />
                      </label>
                    </div>
                    <div class="form-outline mb-3">
                      <label class="form-label" for="sex">Choose your sex
                        <select v-model="form.sexo" class="form-control form-control-lg">
                          <option value="Male" class="form-control rounded-pill">Male</option>
                          <option value="Female" class="form-control rounded-pill">Female</option>
                        </select>
                      </label>
                    </div>
                  </div>

                  <!-- Email -->
                  <div class="form-outline mb-3">
                    <label class="form-label" for="email">Email address
                      <input v-model="form.email" type="email" id="email" class="form-control form-control-lg"
                        required />
                    </label>
                  </div>

                  <!-- Password -->
                  <div class="form-outline mb-3">
                    <label class="form-label" for="password">Password
                      <input v-model="form.contraseña" type="password" id="password"
                        class="form-control form-control-lg" required />
                    </label>
                  </div>

                  <!-- Confirmación -->
                  <div v-if="!isLogin" class="form-outline mb-3">
                    <label class="form-label" for="confPass">Confirm Password
                      <input v-model="form.confPass" type="password" id="confPass" class="form-control form-control-lg"
                        required />
                    </label>
                  </div>

                  <!-- Checkbox -->
                  <div class="form-check mb-3">
                    <input v-model="rememberMe" type="checkbox" id="rememberMe" class="form-check-input" />
                    <label class="form-check-label" for="rememberMe">Remember me</label>
                  </div>
                  

                  <!-- Botón enviar -->
                  <div class="pt-1 mb-3">
                    <button class="btn btn-dark btn-lg btn-block" type="submit">
                      {{ isLogin ? 'Login' : 'Register' }}
                    </button>
                  </div>

                  <!-- Cambiar modo -->
                  <p class="mb-2" style="color: #393f81;">
                    {{ isLogin ? "Don't have an account?" : 'Already have an account?' }}
                    <a href="#" @click.prevent="toggleFormulario" style="color: #393f81;">
                      {{ isLogin ? 'Register here' : 'Login here' }}
                    </a>
                  </p>
                  
                </form>
                <p class="mb-2" style="color: #393f81;" @click="sendEmailForgot">
                    Do you forgot you password
                    <a href="#" style="color: #393f81;">
                      Recover here
                    </a>
                  </p>

                <!-- Mostrar banner de error si las credenciales son incorrectas -->
                <div v-if="errorMessage" class="alert alert-danger mt-3" role="alert">
                  {{ errorMessage }}
                </div>

              </div>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </section>
</template>

<style scoped>
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.4s ease;
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

.alert {
  text-align: center;
  font-size: 14px;
  margin-top: 20px;
  transition: opacity 0.5s ease;
}

body.dark-mode {
  background-color: #18191a !important;
  color: #e4e6eb;
}

body.dark-mode .container {
  background: transparent;
  color: #e4e6eb;
}

body.dark-mode .card {
  background-color: #242526 !important;
  color: #e4e6eb;
  box-shadow: 0 2px 16px rgba(0,0,0,0.7);
}

body.dark-mode .card-body {
  color: #e4e6eb;
}

body.dark-mode .form-label {
  color: #b0b3b8;
}

body.dark-mode .form-control,
body.dark-mode .form-control-lg {
  background-color: #3a3b3c;
  color: #e4e6eb;
  border: 1px solid #555;
}

body.dark-mode .form-control:focus,
body.dark-mode .form-control-lg:focus {
  background-color: #484a4d;
  color: #fff;
  border-color: #1877f2;
  box-shadow: 0 0 0 2px #1877f2;
}

body.dark-mode select.form-control {
  background-color: #3a3b3c;
  color: #e4e6eb;
}

body.dark-mode .btn-dark {
  background-color: #1877f2;
  border-color: #1877f2;
  color: #fff;
  transition: background 0.3s;
}

body.dark-mode .btn-dark:hover,
body.dark-mode .btn-dark:focus {
  background-color: #0056b3;
  border-color: #0056b3;
  color: #fff;
}

body.dark-mode .alert-danger {
  background-color: #2d2d2d;
  color: #ffb3b3;
  border-color: #ff4d4d;
}

body.dark-mode .fw-bold,
body.dark-mode .fs-1,
body.dark-mode .fs-5,
body.dark-mode .text-black,
body.dark-mode .text-muted {
  color: #e4e6eb !important;
}

body.dark-mode a,
body.dark-mode a:visited {
  color: #8ab4f8 !important;
}

body.dark-mode .form-check-label {
  color: #b0b3b8;
}
body.dark-mode section {
  background-color: rgb(59, 61, 49);
}
section {
  background-color: #9A616D;
}
</style>
