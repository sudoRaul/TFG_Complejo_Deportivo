<template>
    <div id="carouselExampleFade" class="carousel slide carousel-fade" data-bs-ride="carousel">
  <div class="carousel-inner">
    <div class="carousel-item active">
      <img src="@/images/imagenPabeCarrusel.jpg" class="d-block w-100 carousel-image" alt="Imagen Pabellón">
    </div>
    <div class="carousel-item">
      <img src="@/images/imagenGimnasioCarrusel.jpg" class="d-block w-100 carousel-image" alt="Imagen gimnasio">
    </div>
    <div class="carousel-item">
      <img src="@/images/imagenTenisCarrusel.jpg" class="d-block w-100 carousel-image" alt="Imagen tenis">
    </div>
  </div>
  <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleFade" data-bs-slide="prev">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Previous</span>
  </button>
  <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleFade" data-bs-slide="next">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Next</span>
  </button>
</div>


</template>
<style scoped>
    .carousel-image {
    object-fit: cover;
    height: 400px;
  }
</style>