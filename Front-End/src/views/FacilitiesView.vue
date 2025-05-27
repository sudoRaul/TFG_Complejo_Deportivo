<script setup>
  import { ref, onMounted, computed } from 'vue'
  import { useRouter } from 'vue-router'
  
  
  const router = useRouter()
  const instalaciones = ref([])
  const loading = ref(true) // Nueva bandera de carga

// Cogemos el token para evitar que se pueda entrar en otras vistas
const token = sessionStorage.getItem("token") || localStorage.getItem("token") || null;

// Redireccianamos al home si no es admin registrado
if (!token) {
  router.push("/");
}
  
  
  onMounted(async () => {
    // Fetch data from the API
    try {
      // Fetch data from the API
      const response = await fetch("http://localhost:5000/instalaciones")
      instalaciones.value = await response.json()
    } catch (error) {
      console.error("Error al cargar las instalaciones:", error)
    } finally {
      loading.value = false // Una vez cargados los datos, marcamos como ya cargado
    }
  })
  
  // Agrupar instalaciones por categoría
  const instalacionesPorCategoria = computed(() => {
    const agrupadas = {}
  
    instalaciones.value.forEach((instalacion) => {
      const categoria = instalacion.categoria.toLowerCase()
      if (!agrupadas[categoria]) {
        agrupadas[categoria] = []
      }
      agrupadas[categoria].push(instalacion)
    })
  
    return agrupadas
  })
  
  // Redirige al hacer clic en una categoría
  function verCategoria(categoria) {
    router.push(`/facilities/${categoria}`)
  }
  </script>

<template>
  <div class="container mt-5">
    
    <h2 class="text-center mb-5">Categories of Facilities</h2>

    <!-- Condición de carga -->
    <div v-if="loading" class="text-center">
      <div class="spinner-border text-success" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    
    <div v-if="instalacionesPorCategoria" class="row justify-content-center">
      <div
        v-for="(instalaciones, categoria) in instalacionesPorCategoria"
        :key="categoria"
        class="col-12 col-md-6 col-lg-4 mb-4"
      >
        <div
          class="card h-100 shadow-sm categoria-card"
          @click="verCategoria(categoria)"
          style="cursor: pointer;"
        >
          <img
            :src= "instalaciones[0]?.foto"
            class="card-img-top"
            alt="Imagen de {{ categoria }}"
          />
          <div class="card-body text-center">
            <h5 class="card-title text-capitalize">{{ categoria }}</h5>
            <p class="card-text text-muted">
              {{ instalaciones.length }} facilities
            </p>
          </div>
        </div>
      </div>
    </div>
    <NoData v-else mensaje="No hay instalaciones para mostrar" submensaje="Revise esta sección en otro momento" />
  </div>
</template>

<style scoped>
.categoria-card {
  transition: transform 0.2s, box-shadow 0.2s;
}
.categoria-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0.75rem 1.5rem rgba(0, 0, 0, 0.2);
}
.card-img-top {
  height: 200px;
  object-fit: cover;
}
</style>
