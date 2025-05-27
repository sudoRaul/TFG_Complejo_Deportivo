<script setup>
import { defineProps } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

// Definimos las props para personalizar el componente
defineProps({
  mensaje: String,
  submensaje: String,
  mostrarBoton: {
    type: Boolean,
    default: true
  },
  textoBoton: {
    type: String,
    default: "Volver al inicio"
  },
  destino: {
    type: String,
    default: "/"
  }
});
</script>


<template>
    <div class="no-data-container text-center">
        <h2 class="mt-3">¡Ups! Something was wrong</h2>
      <img src="@/images/noData.avif" alt="No data image" class="img-fluid" style="max-width: 350px;">
      <h3 class="mt-3">{{ mensaje || "There is not information" }}</h3>
      <p>{{ submensaje || "Try it later." }}</p>
      <button v-if="mostrarBoton" class="btn btn-primary mb-5" @click="router.push(destino)">
        {{ textoBoton }}
      </button>
    </div>
  </template>
  
 
  
  <style scoped>
  .no-data-container {
    margin-top: 50px;
  }
  </style>
  