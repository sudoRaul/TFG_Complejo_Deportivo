<script setup>
import { ref, onMounted } from "vue";
import { Doughnut } from 'vue-chartjs';
import {
    Chart,
    ArcElement,
    Tooltip,
    Legend
} from 'chart.js';
import router from "@/router";


// Cogemos el rol y el token para evitar que se pueda entrar en otras vistas
const sesion = sessionStorage.getItem("usuario") || localStorage.getItem("usuario");
const token = sessionStorage.getItem("token") || localStorage.getItem("token") || null;
const rol = sesion ? JSON.parse(sesion).rol : null;

// Redireccianamos al home si no es admin registrado
if (rol !== "admin" || !token) {
  router.push("/");
}

Chart.register(ArcElement, Tooltip, Legend);

const usuarios = ref([]);
const edadMedia = ref(0);
const gruposEdad = ref([0, 0, 0]); // [<30, 30-50, >50]
const gruposGenero = ref([0, 0]); // [Masculino, Femenino]

async function obtenerUsuarios() {
    try {
        const response = await fetch("http://127.0.0.1:5000/usuarios/");
        if (!response.ok) throw new Error("Error obtaining users");
        usuarios.value = await response.json();
        if (usuarios.value.length > 0) {
            edadMedia.value = (
                usuarios.value.reduce((acc, elem) => acc + elem.edad, 0) / usuarios.value.length
            ).toFixed(1);
            // Calcular grupos de edad
            gruposEdad.value = [
                usuarios.value.filter(u => u.edad < 30).length,
                usuarios.value.filter(u => u.edad >= 30 && u.edad <= 50).length,
                usuarios.value.filter(u => u.edad > 50).length
            ];
            // Calcular grupos de género
            gruposGenero.value = [
                usuarios.value.filter(u => u.sexo === 'Male').length,
                usuarios.value.filter(u => u.sexo === 'Female').length
            ];
        }
    } catch (err) {
        console.error(err.message);
    }
}

onMounted(() => {
    obtenerUsuarios();
});
</script>

<template>
    <div v-if="usuarios" class="container py-4">
        <h1 class="mb-4 text-center">Users' statistics</h1>
        <div class="mb-3 text-center mb-5">
            <h3>Users' average age: <span class="text-primary">{{ edadMedia }}</span> años</h3>
        </div>
        <div class="row flex justify-content-around">
            <div class="col-sm-10 col-md-6 col-lg-4 mb-4">
                <Doughnut :data="{
                    labels: ['Younger than 30', '30 to 50', 'Older than 50'],
                    datasets: [{
                        data: gruposEdad,
                        backgroundColor: ['#36A2EB', '#FFCE56', '#FF6384'],
                        borderWidth: 2
                    }]
                }" :options="{
            responsive: true,
            plugins: {
                legend: { position: 'bottom' },
                tooltip: { enabled: true }
            }
        }" />
                <div class="text-center mt-2">
                    <span class="badge bg-primary">Younger than 30: {{ gruposEdad[0] }}</span>
                    <span class="badge bg-warning ms-2" style="background-color:#F76FA1;color:#fff;">Between 30 and 50:
                        {{ gruposEdad[1] }}</span>
                    <span class="badge bg-pink ms-2" style="background-color:#F76FA1;color:#fff;">Older than 50: {{
                        gruposEdad[2] }}</span>

                </div>
            </div>
            <div class="col-sm-10 col-md-6 col-lg-4 mb-4">
                <Doughnut :data="{
                    labels: ['Male', 'Female'],
                    datasets: [{
                        data: gruposGenero,
                        backgroundColor: ['#4F8EF7', '#F76FA1'],
                        borderWidth: 2
                    }]
                }" :options="{
            responsive: true,
            plugins: {
                legend: { position: 'bottom' },
                tooltip: { enabled: true }
            }
        }" />
                <div class="text-center mt-2">
                    <span class="badge bg-primary">Male: {{ gruposGenero[0] }}</span>
                    <span class="badge bg-pink ms-2" style="background-color:#F76FA1;color:#fff;">Female: {{
                        gruposGenero[1] }}</span>
                </div>
            </div>
        </div>
    </div>
    <NoData v-else mensaje="There isn't users to show" submensaje="Inspect this section later" />

</template>