<script setup>
import { Line } from 'vue-chartjs';
import {
    Chart as ChartJS,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js';

ChartJS.register(LineElement, PointElement, CategoryScale, LinearScale, Title, Tooltip, Legend);

const props = defineProps({
    chartData: Object,
    chartOptions: Object
});
</script>
<template>
    <Line :data="chartData" :options="chartOptions" />
</template>
