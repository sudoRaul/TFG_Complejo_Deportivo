<script setup>
import { defineProps } from "vue";

defineProps({
  titulo: String,
  descripcion: String,
  icono: String,
  colorFondo: {
    type: String,
    default: "bg-success"
  },
  textColor: {
    type: String,
    default: "text-white"
  },
  altText: {
    type: String,
    default: "Icono descriptivo"
  }
});
</script>

<template>
  <div 
    class="tarjeta-informativa d-flex align-items-center p-4 rounded shadow-sm mb-3 h-100 transition-all"
    :class="[colorFondo, textColor]"
  >
    <div 
      v-if="icono" 
      class="bg-white bg-opacity-25 rounded-circle d-flex align-items-center justify-content-center me-4" 
      style="width: 60px; height: 60px; flex-shrink: 0;"
    >
      <img 
        :src="typeof icono === 'string' ? icono : icono.src" 
        :alt="altText"
        class="img-fluid"
        style="max-width: 80%; max-height: 80%; object-fit: contain;"
      />
    </div>
    <div class="contenido">
      <h3 class="h5 fw-semibold mb-2">{{ titulo }}</h3>
      <p class="mb-0 opacity-90">{{ descripcion }}</p>
    </div>
  </div>
</template>

<style scoped>
.transition-all {
  transition: all 0.3s ease;
}

.tarjeta-informativa:hover {
  transform: translateY(-5px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}

/* Ajustes para móviles */
@media (max-width: 768px) {
  .tarjeta-informativa {
    flex-direction: column !important;
    text-align: center !important;
    padding: 1.5rem !important;
  }
  
  .tarjeta-informativa > div:first-child {
    margin-right: 0 !important;
    margin-bottom: 1rem !important;
  }
}
</style>