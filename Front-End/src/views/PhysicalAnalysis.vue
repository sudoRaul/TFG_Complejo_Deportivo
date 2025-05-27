<script setup>
import { ref, onMounted, computed } from 'vue';
import Swal from 'sweetalert2';
import BarChart from '@/components/BarChart.vue';
import LineChart from '@/components/LineChart.vue'; // Importing Line Chart
import HorizontalBarChart from '@/components/HorizontalBarChart.vue'; // Importing Horizontal Bar Chart
import router from "@/router";


const token = sessionStorage.getItem("token") || localStorage.getItem("token") || null;

// Redireccianamos al home si no es admin registrado
if (!token) {
  router.push("/");
}

const usuario = ref(null);
const sesion = sessionStorage.getItem("usuario") || localStorage.getItem("usuario");
const id = sesion ? JSON.parse(sesion).id : null;
const actividad = ref('1.2');
const resultado = ref({});

const cargarDatosUsuario = async () => {
    try {
        if (!id) {
            Swal.fire({ icon: 'error', title: 'Error', text: 'No se pudo encontrar el ID de usuario.' });
            return;
        }

        const response = await fetch(`http://127.0.0.1:5000/usuarios/${id}`);
        if (!response.ok) throw new Error('Error obtaining users datas.');

        usuario.value = await response.json();

    } catch (error) {
        Swal.fire({ icon: 'error', title: 'Error', text: error.message });
    }
};

const calcularIMCClasificacion = (imc) => {
    if (imc < 18.5) return 'Underweight';
    else if (imc < 25) return 'Normal weight';
    else if (imc < 30) return 'Overweight';
    else return 'Obesity';
};

const calcularIMC = () => {
    const peso = usuario.value.peso;
    const alturaM = usuario.value.altura / 100;
    const imc = peso / (alturaM * alturaM);
    const imcClasificacion = calcularIMCClasificacion(imc);
    resultado.value.imc = imc;
    resultado.value.imcClasificacion = imcClasificacion;
};

const calcularFCM = () => {
    const edad = usuario.value.edad;
    resultado.value.fcm = 220 - edad;
};

const calcularTMB_GET = () => {
    const peso = usuario.value.peso;
    const altura = usuario.value.altura;
    const edad = usuario.value.edad;
    const sexo = usuario.value.sexo;

    const tmb = sexo === 'Male'
        ? 10 * peso + 6.25 * altura - 5 * edad + 5
        : 10 * peso + 6.25 * altura - 5 * edad - 161;

    const get = tmb * parseFloat(actividad.value);

    resultado.value.tmb = tmb;
    resultado.value.get = get;
};

// TMB vs GET Chart Data
const chartData = computed(() => {
    if (!resultado.value?.tmb) return null;
    return {
        labels: ['TMB', 'GET'],
        datasets: [{
            label: 'Calories (kcal)',
            backgroundColor: ['#36A2EB', '#FF6384'],
            data: [resultado.value.tmb, resultado.value.get]
        }]
    };
});

const chartOptions = {
    responsive: true,
    plugins: {
        legend: { display: true },
        title: { display: true, text: 'TMB vs GET Comparison' }
    }
};

// FCM Zones Chart Data
const chartDataFCM = computed(() => {
    if (!resultado.value?.fcm) return null;
    const fcm = resultado.value.fcm;
    return {
        labels: ['Zone 1', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone 5'],
        datasets: [{
            label: 'Training Zones (bpm)',
            data: [
                fcm * 0.6,
                fcm * 0.7,
                fcm * 0.8,
                fcm * 0.9,
                fcm
            ],
            fill: false,
            borderColor: '#36A2EB',
            tension: 0.4
        }]
    };
});

const chartOptionsFCM = {
    responsive: true,
    plugins: {
        title: {
            display: true,
            text: 'Heart Rate Training Zones (in bpm)'
        },
        legend: {
            display: false
        }
    },
    scales: {
        y: {
            beginAtZero: true,
            title: {
                display: true,
                text: 'Beats per minute'
            }
        }
    }
};

// IMC Classification Chart Data
const chartDataIMC = computed(() => {
    if (!resultado.value?.imc) return null;
    const actual = resultado.value.imc.toFixed(2);
    return {
        labels: ['Underweight', 'Normal', 'Overweight', 'Obesity'],
        datasets: [{
            label: 'IMC',
            data: [18.4, 24.9, 29.9, 40],
            backgroundColor: ['#36A2EB', '#4BC0C0', '#FFCE56', '#FF6384']
        },
        {
            label: 'Your IMC',
            data: [actual, actual, actual, actual],
            backgroundColor: ['#00000080', '#00000080', '#00000080', '#00000080']
        }]
    };
});

const chartOptionsIMC = {
    indexAxis: 'y',
    responsive: true,
    plugins: {
        title: {
            display: true,
            text: 'IMC Classification by WHO'
        },
        legend: {
            position: 'bottom'
        }
    },
    scales: {
        x: {
            beginAtZero: true,
            max: 40
        }
    }
};


onMounted(() => {
    cargarDatosUsuario();
});
</script>

<template>
    <div class="container my-5">
        <h2 class="text-center mb-4">Physical Analysis</h2>

        <div class="row d-flex justify-content-around text-center">
            <!-- 1. User Information -->
            <div v-if="usuario" class="card p-4 shadow-sm mb-4 col-md-5 col-xs-6 d-flex flex-column izqContainer ">
                <h5 class="card-title">User Information</h5>
                <div><strong>Name: {{ usuario.nombre }}</strong></div>
                <div><strong>Age: {{ usuario.edad }} years</strong></div>
                <div><strong>Gender: {{ usuario.sexo === 'Male' ? 'Male' : 'Female' }}</strong></div>
                <div><strong>Weight: {{ usuario.peso }} kg</strong></div>
                <div><strong>Height: {{ usuario.altura }} cm</strong></div>
            </div>

            <!-- 2. IMC -->
            <div v-if="usuario" class="card p-4 shadow-sm mb-4 col-md-5 col-xs-6 d-flex flex-column imc">
                <h5 class="card-title">Body Mass Index (IMC)</h5>
                <br>
                <small class="text-muted">
                    IMC is a value that relates weight to height. It serves as a general estimation of bodily health.
                </small>
                <br>
                <button @click="calcularIMC" class="btn btn-outline-primary mb-3">Calculate IMC</button>
                <div v-if="resultado?.imc">
                    <p><strong>IMC:</strong> {{ resultado.imc.toFixed(2) }}</p>
                    <p><strong>Classification:</strong> {{ resultado.imcClasificacion }}</p>

                    <!-- IMC Chart -->
                    <HorizontalBarChart v-if="chartDataIMC" :chart-data="chartDataIMC" :chart-options="chartOptionsIMC"
                        class="my-3" />
                </div>
            </div>

            <!-- 3. Maximum Heart Rate (FCM) -->
            <div v-if="usuario" class="card p-4 shadow-sm mb-4 col-md-5 col-xs-6 d-flex flex-column fcm">
                <h5 class="card-title">Maximum Heart Rate (FCM)</h5>
                <br>
                <small class="text-muted">
                    FCM is the maximum heart rate your heart can reach during exercise. It is estimated as 220 - age.
                </small>
                <br>
                <button @click="calcularFCM" class="btn btn-outline-success mb-3">Calculate FCM</button>
                <div v-if="resultado?.fcm">
                    <p><strong>FCM:</strong> {{ resultado.fcm }} bpm</p>
                    <small class="text-muted">
                        <ul id="lista">
                            <li>Zone 1: Warm-up Zone</li>
                            <li>Zone 2: Fat Burning Zone</li>
                            <li>Zone 3: Endurance Zone</li>
                            <li>Zone 4: Threshold Zone</li>
                            <li>Zone 5: Maximum Zone</li>
                        </ul>
                    </small>

                    <!-- FCM Zones Chart -->
                    <LineChart v-if="chartDataFCM" :chart-data="chartDataFCM" :chart-options="chartOptionsFCM"
                        class="my-3" />
                </div>
            </div>

            <!-- 4. TMB vs GET -->
            <div v-if="usuario" class="card p-4 shadow-sm mb-4 col-md-5 col-xs-6 d-flex flex-column tmb">
                <h5 class="card-title">Basal Metabolic Rate (TMB) vs Total Energy Expenditure (GET)</h5>

                <small class="text-muted">
                    Basal Metabolic Rate (TMB) is the minimum energy your body needs at rest. Total Energy Expenditure
                    (GET) also includes physical activity. GET = TMB × Activity Factor.
                </small>
                <br>
                <div class="mb-3">
                    <label class="form-label"><strong>Physical Activity Level</strong></label>
                    <select v-model="actividad" class="form-select">
                        <option value="1.2">Sedentary</option>
                        <option value="1.375">Lightly active</option>
                        <option value="1.55">Moderately active</option>
                        <option value="1.725">Very active</option>
                        <option value="1.9">Extremely active</option>
                    </select>
                </div>

                <button @click="calcularTMB_GET" class="btn btn-outline-warning mb-3">Calculate TMB and GET</button>

                <div v-if="resultado?.tmb">
                    <p><strong>TMB:</strong> {{ resultado.tmb.toFixed(2) }} kcal</p>
                    <p><strong>GET:</strong> {{ resultado.get.toFixed(2) }} kcal</p>

                    <!-- TMB vs GET Chart -->
                    <BarChart :chart-data="chartData" :chart-options="chartOptions" class="my-3" />
                </div>
            </div>
        </div>
    </div>
</template>
<style>
.analysis-card {
    border-radius: 1.2rem;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    transition: background 0.3s, color 0.3s;
}

/* Modo claro */
.izqContainer {
    background: linear-gradient(135deg, #fff6f3 60%, #ffeceb 100%);
}

.imc {
    background: linear-gradient(135deg, #e6fafd 60%, #d3f6f6 100%);
}

.fcm {
    background: linear-gradient(135deg, #e6fbe6 60%, #d9f9e2 100%);
}

.tmb {
    background: linear-gradient(135deg, #fffde4 60%, #fff9c4 100%);
}

.card-title {
    font-weight: 700;
}

ul {
    padding-left: 1.2em;
}

ul li {
    margin-bottom: 0.3em;
}

/* Modo oscuro */
body.dark-mode {
    background-color: #18191a !important;
    color: #e4e6eb;
}

body.dark-mode .analysis-card {
    background: #23272f !important;
    color: #e4e6eb !important;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.7);
}

body.dark-mode .izqContainer {
    background: linear-gradient(135deg, #2d2d3a 60%, #23272f 100%) !important;
}

body.dark-mode .imc {
    background: linear-gradient(135deg, #23343a 60%, #1e2a2e 100%) !important;
}

body.dark-mode .fcm {
    background: linear-gradient(135deg, #233a2a 60%, #1e2e23 100%) !important;
}

body.dark-mode .tmb {
    background: linear-gradient(135deg, #3a3923 60%, #2e2c1e 100%) !important;
}

body.dark-mode .card-title,
body.dark-mode strong {
    color: #f3f3f3 !important;
}

body.dark-mode .form-select,
body.dark-mode .form-select:focus {
    background: #23272f !important;
    color: #e4e6eb !important;
    border: 1px solid #444 !important;
}

body.dark-mode .btn-outline-primary,
body.dark-mode .btn-outline-success,
body.dark-mode .btn-outline-warning {
    color: #e4e6eb !important;
    border-color: #1877f2 !important;
}

body.dark-mode .btn-outline-primary:hover,
body.dark-mode .btn-outline-success:hover,
body.dark-mode .btn-outline-warning:hover {
    background: #1877f2 !important;
    color: #fff !important;
    border-color: #1877f2 !important;
}

body.dark-mode .text-muted {
    color: #b0b3b8 !important;
}

body.dark-mode div{
    color:white !important;
}

#lista{
    list-style-type: none;
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