<script setup>
import { ref, onMounted } from 'vue';
import NoData from '@/components/NoData.vue';
import Swal from 'sweetalert2';
import router from "@/router";


const token = sessionStorage.getItem("token") || localStorage.getItem("token") || null;

// Redireccianamos al home si no es admin registrado
if (!token) {
  router.push("/");
}

const reservas = ref([]);
const loading = ref(true);
const reservaSeleccionada = ref(null);
const nuevaFecha = ref(null);
const nuevaHora = ref("");


// Generar array de horas válidas (08:00 a 21:00)
const horasDisponibles = [];
for (let h = 8; h <= 21; h++) {
    const horaStr = h.toString().padStart(2, '0') + ":00";
    horasDisponibles.push(horaStr);
}

const sesion = JSON.parse(sessionStorage.getItem("usuario") || localStorage.getItem("usuario") || null);
const email = sesion ? sesion.email : null;

const fetchReservas = async () => {
    loading.value = true;
    try {
        const response = await fetch(`http://127.0.0.1:5000/reservas/usuario?email=${email}`);
        const data = await response.json();
        reservas.value = Array.isArray(data) ? data : [];
    } catch (error) {
        console.error('Error loading reserves:', error);
        reservas.value = [];
    } finally {
        loading.value = false;
    }
};

onMounted(() => {
    if (email) {
        fetchReservas();
    } else {
        loading.value = false;
    }
});

const formatFecha = (fechaISO) => {
    if (!fechaISO) return '';
    const opciones = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(fechaISO).toLocaleDateString('es-ES', opciones);
};

// Validación de si se puede editar
const puedeEditar = (fecha, hora) => {
    const ahora = new Date();
    const fechaHoraReserva = new Date(`${fecha}T${hora}`);
    const diffHoras = (fechaHoraReserva - ahora) / (1000 * 60 * 60);
    return diffHoras >= 24;
};

// Editar reserva: mostrar modal o SweetAlert
const editarReserva = (reserva) => {
    if (!puedeEditar(reserva.fecha, reserva.hora)) {
        Swal.fire({
            icon: 'error',
            title: 'You cannot edit',
            text: 'You cannot edit a reservation with less than 24 hours notice.',
        });
        return;
    }

    reservaSeleccionada.value = reserva;
    nuevaFecha.value = reserva.fecha;
    nuevaHora.value = reserva.hora;

    const modal = new bootstrap.Modal(document.getElementById('editarReservaModal'));
    modal.show();
};

// Validación y guardado
const validarYGuardarReserva = async () => {
    const ahora = new Date();
    const fechaHoraNueva = new Date(`${nuevaFecha.value}T${nuevaHora.value}`);
    const diferenciaHoras = (fechaHoraNueva - ahora) / (1000 * 60 * 60);

    if (diferenciaHoras < 24) {
        Swal.fire({
            icon: 'error',
            title: 'You cannot edit',
            text: 'You cannot edit a reservation with less than 24 hours notice.',
        });
        return;
    }

    if (fechaHoraNueva < ahora) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid date',
            text: 'You cannot edit a reservation that has already passed.',
        });
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/reservas/${reservaSeleccionada.value.id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                fecha: nuevaFecha.value,
                hora: nuevaHora.value
            })
        });

        if (response.ok) {
            Swal.fire('Éxito', 'Reserve updated succesfully.', 'success');
            const modal = bootstrap.Modal.getInstance(document.getElementById('editarReservaModal'));
            modal.hide();
            fetchReservas();
        } else {
            Swal.fire('Error', 'There was a problem updating the reserve', 'error');
        }
    } catch (error) {
        console.error('Error updating the reserve:', error);
        Swal.fire('Error', 'There was a problem savinng the changes', 'error');
    }
};

const cancelarReserva = async (reservaID, fecha, hora) => {
    const ahora = new Date();
    const fechaHoraReserva = new Date(`${fecha}T${hora}`);
    const diferenciaHoras = (fechaHoraReserva - ahora) / (1000 * 60 * 60);

    if (diferenciaHoras < 24) {
        Swal.fire({
            icon: 'error',
            title: 'You cannot delete',
            text: 'You cannot cancel a reservation with less than 24 hours notice.',
        });
        return;
    }

    if (fechaHoraReserva < ahora) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid date',
            text: 'You cannot cancel a reservation that has already passed.',
        });
        return;
    }

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
            const response = await fetch(`http://127.0.0.1:5000/reservas/${reservaID}`, {
                method: "DELETE",
            });

            if (!response.ok) throw new Error("Error al eliminar la reserva");

            Swal.fire({
                icon: "success",
                title: "Reserve deleted",
                text: "Your reservation has been successfully deleted.",
                timer: 2000,
                showConfirmButton: false,
            });

            fetchReservas();
        } catch (err) {
            console.error(err.message);
            Swal.fire('Error', 'There was a problem deleting your reserve.', 'error');
        }
    }
};
</script>

<template>
    <div class="container py-5">
        <h2 class="text-center mb-4">My reservations</h2>

        <div v-if="loading" class="text-center my-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>

        <NoData
            v-else-if="!reservas.length"
            mensaje="You haven't made any reservations yet"
            submensaje="You can book facilities from the facilities section."
            textoBoton="Go to facilities"
            destino="/facilities"
        />

        <div v-else class="row g-4 justify-content-center">
            <div v-for="reserva in reservas" :key="reserva.id" class="col-12 col-md-6 d-flex">
                <div class="card h-100 shadow rounded-4 w-100">
                    <img
                        :src="reserva.instalacion.foto"
                        class="card-img-top rounded-top-4"
                        alt="Image of facility"
                        style="object-fit: cover; height: 200px;"
                        @error="event.target.src = 'https://via.placeholder.com/400x200?text=Sin+Imagen'"
                    >
                    <div class="card-body d-flex flex-column justify-content-between">
                        <div>
                            <h5 class="card-title text-primary">{{ reserva.instalacion.nombre }}</h5>
                            <p class="text-muted mb-2"><em>{{ reserva.instalacion.categoria }}</em></p>
                            <p class="card-text">{{ reserva.instalacion.descripcion }}</p>
                            <hr>
                            <p class="card-text mb-1">
                                <strong>Date:</strong> {{ formatFecha(reserva.fecha) }}
                            </p>
                            <p class="card-text mb-1">
                                <strong>Time:</strong> {{ reserva.hora }}
                            </p>
                        </div>
                        <div class="mt-3 row g-2">
                            <div class="col-6">
                                <button class="btn btn-outline-danger w-100" @click="cancelarReserva(reserva.id, reserva.fecha, reserva.hora)">
                                    Cancel
                                </button>
                            </div>
                            <div class="col-6">
                                <button class="btn btn-outline-warning w-100" @click="editarReserva(reserva)">
                                    Edit
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modal para editar la reserva -->
        <div class="modal fade" id="editarReservaModal" tabindex="-1" aria-labelledby="editarReservaModalLabel"
            aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="editarReservaModalLabel">Edit Reserve</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Cerrar"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label for="fecha" class="form-label">New Date</label>
                            <input type="date" v-model="nuevaFecha" class="form-control"
                                :min="new Date().toISOString().split('T')[0]" />
                        </div>
                        <div class="mb-3">
                            <label for="hora" class="form-label">New Time</label>
                            <select v-model="nuevaHora" class="form-select">
                                <option disabled value="">Select a time</option>
                                <option v-for="hora in horasDisponibles" :key="hora" :value="hora">
                                    {{ hora }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" @click="validarYGuardarReserva">Save
                            changes</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
.card-title {
    font-weight: 600;
}
.card {
    border-radius: 1.5rem;
    transition: box-shadow 0.3s;
}
.card-img-top {
    border-top-left-radius: 1.5rem;
    border-top-right-radius: 1.5rem;
}
body.dark-mode .card {
    background: #23272f !important;
    color: #e4e6eb !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.7);
}
body.dark-mode .card-title,
body.dark-mode .card-text,
body.dark-mode .text-muted,
body.dark-mode strong {
    color: #e4e6eb !important;
}
body.dark-mode .btn-outline-danger {
    color: #ff7675 !important;
    border-color: #ff7675 !important;
}
body.dark-mode .btn-outline-danger:hover {
    background: #ff7675 !important;
    color: #fff !important;
}
body.dark-mode .btn-outline-warning {
    color: #ffe066 !important;
    border-color: #ffe066 !important;
}
body.dark-mode .btn-outline-warning:hover {
    background: #ffe066 !important;
    color: #23272f !important;
}
body.dark-mode .modal-content {
    background: #23272f !important;
    color: #e4e6eb !important;
}
body.dark-mode .form-control,
body.dark-mode .form-select {
    background: #23272f !important;
    color: #e4e6eb !important;
    border: 1px solid #444 !important;
}
body.dark-mode .form-control:focus,
body.dark-mode .form-select:focus {
    background: #23272f !important;
    color: #fff !important;
    border-color: #1877f2 !important;
    box-shadow: 0 0 0 2px #1877f2;
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