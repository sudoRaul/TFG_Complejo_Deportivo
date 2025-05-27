<script setup>
import { ref, computed, onMounted } from "vue";
import Swal from "sweetalert2";
import router from "@/router";

// Inicializamos el array de usuarios y los roles disponibles
const usuarios = ref([]);
const rolesDisponibles = ["admin", "usuario"];

// Cogemos el rol y el token para evitar que se pueda entrar en otras vistas
const sesion = sessionStorage.getItem("usuario") || localStorage.getItem("usuario");
const token = sessionStorage.getItem("token") || localStorage.getItem("token") || null;
const rol = sesion ? JSON.parse(sesion).rol : null;

// Redireccianamos al home si no es admin registrado
if (rol !== "admin" || !token) {
  router.push("/");
}

// Constantes para la paginación
const usuariosPorPagina = 5;
const paginaActual = ref(1);

// Obtenemos los usuarios de la BBDD
async function obtenerUsuarios() {
  try {
    const response = await fetch("http://127.0.0.1:5000/usuarios/");
    if (!response.ok) throw new Error("Error obtaining users");
    usuarios.value = await response.json();
  } catch (err) {
    console.error(err.message);
  }
}

// Actualizamos el rol
async function actualizarRol(usuarioId, nuevoRol) {
  try {
    const response = await fetch(`http://127.0.0.1:5000/usuarios/${usuarioId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ rol: nuevoRol }),
    });

    if (!response.ok) throw new Error("Error updating role");

    Swal.fire({
      icon: "success",
      title: "Role updated",
      text: `User is now ${nuevoRol}`,
      timer: 2000,
      showConfirmButton: false,
    });

    obtenerUsuarios();
  } catch (err) {
    console.error(err.message);
  }
}

// Eliminamos al usuario
async function eliminarUsuario(usuarioId) {
  //Antes de eliminar, mostramos un mensaje de confirmación
  const confirmacion = await Swal.fire({
    title: "Are you sure?",
    text: "This action cannot be undone.",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#d33",
    cancelButtonColor: "#3085d6",
    confirmButtonText: "Yes, delete it",
    cancelButtonText: "Cancel",
  });

  if (confirmacion.isConfirmed) {
    try {
      const response = await fetch(`http://127.0.0.1:5000/usuarios/${usuarioId}`, {
        method: "DELETE",
      });

      if (!response.ok) throw new Error("Error deleting user");

      Swal.fire({
        icon: "success",
        title: "User deleted",
        text: "The user was deleted succesfully.",
        timer: 2000,
        showConfirmButton: false,
      });

      obtenerUsuarios();
    } catch (err) {
      console.error(err.message);
    }
  }
}

//Cogemos el número total de páginas dividiendo el total de usuarios entre los usuarios por pagina
const totalPaginas = computed(() => Math.ceil(usuarios.value.length / usuariosPorPagina));

//Usamos una propiedad computada cuyo valor depende de la página actual y de los usuarios
const usuariosPaginados = computed(() => {
  const inicio = (paginaActual.value - 1) * usuariosPorPagina;
  return usuarios.value.slice(inicio, inicio + usuariosPorPagina);
});

// Cambiamos de página
function cambiarPagina(nuevaPagina) {
  if (nuevaPagina > 0 && nuevaPagina <= totalPaginas.value) {
    paginaActual.value = nuevaPagina;
  }
}

// Cargamos los usuarios 
onMounted(obtenerUsuarios);
</script>

<template>
  <div v-if="usuarios">
    <h2 class="text-center mt-5 mb-4 fs-1">User's administration</h2>

    <table class="table table-striped table-hover mb-5 mt-3">
      <thead>
        <tr class="text-center fs-4">
          <th scope="col" id="id">ID</th>
          <th scope="col" id="name">Name</th>
          <th scope="col" id="age">Age</th>
          <th scope="col" id="rol">Rol</th>
          <th scope="col" id="delete">Delete</th>
        </tr>
      </thead>
      <tbody>
        <tr class="text-center fs-5" v-for="(usuario, index) in usuariosPaginados" :key="usuario.id">
          <td headers="id">{{ usuario.id }}</td>
          <td headers="name">{{ usuario.nombre }}</td>
          <td headers="age">{{ usuario.edad }}</td>
          <td headers="rol">
            <select v-model="usuario.rol" @change="actualizarRol(usuario.id, $event.target.value)" class="form-select"
              :disabled="usuario.id == 1">
              <option v-for="rol in rolesDisponibles" :key="rol" :value="rol">{{ rol }}</option>
            </select>
          </td>
          <td headers="delete">
            <button class="btn btn-danger col-7 mt-1 p-2" @click="eliminarUsuario(usuario.id)"
              :disabled="usuario.id == 1">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>


    <nav aria-label="Paginación de usuarios" class="mb-3 pb-4">
      <ul class="pagination justify-content-center">
        <li class="page-item" :class="{ disabled: paginaActual === 1 }">
          <button class="page-link fs-5" @click="cambiarPagina(paginaActual - 1)">Previous</button>
        </li>

        <li class="page-item" v-for="pagina in totalPaginas" :key="pagina" :class="{ active: pagina === paginaActual }">
          <button class="page-link fs-5" @click="cambiarPagina(pagina)">{{ pagina }}</button>
        </li>

        <li class="page-item" :class="{ disabled: paginaActual === totalPaginas }">
          <button class="page-link fs-5" @click="cambiarPagina(paginaActual + 1)">Next</button>
        </li>
      </ul>
    </nav>
  </div>
  <NoData v-else mensaje="No hay usuarios actualmente" submensaje="Revise esta sección en otro momento" />
</template>

<style>
.btn-danger {
  border-radius: 5px;
  transition: background 0.3s ease;
}

.btn-danger:hover {
  scale: 1.01;
  background-color: #ff0000;
}

body.dark-mode {
  background-color: #18191a !important;
  color: #e4e6eb;
}

body.dark-mode .table {
  background-color: #242526 !important;
  color: #e4e6eb;
}

body.dark-mode .table-striped>tbody>tr:nth-of-type(odd) {
  background-color: #23272b !important;
}

body.dark-mode .table-hover>tbody>tr:hover {
  background-color: #343a40 !important;
  color: #fff;
}

body.dark-mode .form-select {
  background-color: #3a3b3c;
  color: #e4e6eb;
  border: 1px solid #555;
}

body.dark-mode .form-select:focus {
  background-color: #484a4d;
  color: #fff;
  border-color: #1877f2;
  box-shadow: 0 0 0 2px #1877f2;
}

body.dark-mode .btn-danger {
  background-color: #d9534f !important;
  border-color: #d43f3a !important;
  color: #fff !important;
}

body.dark-mode .btn-danger:hover,
body.dark-mode .btn-danger:focus {
  background-color: #ff0000 !important;
  border-color: #ff0000 !important;
  color: #fff !important;
}

body.dark-mode .page-link {
  background-color: #242526 !important;
  color: #e4e6eb !important;
  border: 1px solid #555 !important;
}

body.dark-mode .page-item.active .page-link {
  background-color: #1877f2 !important;
  border-color: #1877f2 !important;
  color: #fff !important;
}

body.dark-mode .page-link:focus {
  box-shadow: 0 0 0 2px #1877f2;
}

body.dark-mode tr {
  background-color: red !important;
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
