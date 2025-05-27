<script setup>
import { Bar } from 'vue-chartjs';
import {
    Chart as ChartJS,
    BarElement,
    CategoryScale,
    LinearScale,
    Title,
    Tooltip,
    Legend
} from 'chart.js';

ChartJS.register(BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend);

const props = defineProps({
    chartData: Object,
    chartOptions: Object
});
</script>
<template>
    <Bar :data="chartData" :options="chartOptions" />
</template>