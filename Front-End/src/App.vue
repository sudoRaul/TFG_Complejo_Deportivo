<script setup>
import { ref, onMounted } from "vue";
import Header from "./components/Header.vue";
import Footer from "./components/Footer.vue";

const usuarioActivo = ref(null);

onMounted(() => {
  const sesion = sessionStorage.getItem("usuario");
  if (sesion) {
    usuarioActivo.value = JSON.parse(sesion);
  }
});

function cerrarSesion() {
  sessionStorage.removeItem("usuario");
  sessionStorage.removeItem("token");
  usuarioActivo.value = null;
}
</script>

<template>
  <Header
    title="La Morada"
    :usuarioAutenticado="usuarioActivo"
    @cerrar-sesion="cerrarSesion"
  />

  <router-view @login-exitoso="usuarioActivo = $event" />

  <Footer />
</template>

<style>
body.dark-mode {
  background-color: #121212;
  color: white;
}
</style>
