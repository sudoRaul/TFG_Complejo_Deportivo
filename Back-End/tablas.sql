-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 02-06-2025 a las 18:53:40
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `complejo_deportivo`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `contacto`
--

CREATE TABLE `contacto` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `comentario` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `contacto`
--

INSERT INTO `contacto` (`id`, `nombre`, `apellido`, `email`, `telefono`, `comentario`) VALUES
(1, 'Juan', 'Gomez', 'juan.gomez@example.com', '555-1010', 'The tennis court is in excellent condition, highly recommended for advanced players.'),
(2, 'Maria', 'Lopez', 'maria.lopez@example.com', '555-2020', 'Are there ligth on the nigth.'),
(3, 'Andres', 'Martinez', 'andres.martinez@example.com', '555-3030', 'Are there balls in the padel court?'),
(4, 'Laura', 'Sanchez', 'laura.sanchez@example.com', '555-4040', 'In the gym there is too hot.'),
(5, 'Pedro', 'Rodriguez', 'pedro.rodriguez@example.com', '555-5050', 'What`s wrong with the swimming pool'),
(7, 'Fulano', 'De Tal', 'fulano@gmail.com', '654123789', 'I mistake in my reserve');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `instalaciones`
--

CREATE TABLE `instalaciones` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `foto` varchar(255) DEFAULT NULL,
  `categoria` varchar(100) NOT NULL,
  `disponibilidad` varchar(20) DEFAULT '1',
  `descripcion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `instalaciones`
--

INSERT INTO `instalaciones` (`id`, `nombre`, `foto`, `categoria`, `disponibilidad`, `descripcion`) VALUES
(1, 'Football Field', 'https://i.pinimg.com/736x/11/4c/a2/114ca22af2272e4b75342b5fa17b65a0.jpg', 'Football', 'yes', 'High-quality football field available for matches and training.'),
(2, 'Tennis Court', 'https://i.pinimg.com/736x/7a/a2/83/7aa283cb931cbf0857ec7bb323925daf.jpg', 'Tennis', 'yes', 'Professional tennis court, ideal for advanced players.'),
(3, 'Basket Field', 'https://i.pinimg.com/736x/10/12/aa/1012aad2f6a11cd179e11daf65819fad.jpg', 'Basket', 'no', 'Special basket field, here trined Lebron James'),
(4, 'Padel Court', 'https://i.pinimg.com/736x/ed/d0/f2/edd0f2edc880287dfc56fa4b7a355757.jpg', 'Padel', 'yes', 'Fantastic padel court'),
(5, 'Gym', 'https://i.pinimg.com/736x/db/e6/10/dbe61002bf872ef32ad3865245375b4e.jpg', 'Gym', 'yes', 'Train all your muscles on this ');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reservas`
--

CREATE TABLE `reservas` (
  `id` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `id_instalacion` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `hora` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `reservas`
--

INSERT INTO `reservas` (`id`, `id_usuario`, `id_instalacion`, `fecha`, `hora`) VALUES
(1, 1, 1, '2025-06-01', '10:00:00'),
(2, 2, 2, '2025-06-02', '15:30:00'),
(3, 3, 3, '2025-06-03', '09:00:00'),
(4, 4, 4, '2025-06-04', '18:00:00'),
(5, 5, 5, '2025-06-05', '12:00:00'),
(24, 54, 1, '2025-05-27', '20:00:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `edad` int(11) NOT NULL,
  `rol` varchar(50) NOT NULL CHECK (`rol` in ('admin','usuario')),
  `altura` int(11) DEFAULT NULL,
  `peso` int(11) DEFAULT NULL,
  `sexo` varchar(12) DEFAULT NULL,
  `telefono` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `apellido`, `email`, `contraseña`, `edad`, `rol`, `altura`, `peso`, `sexo`, `telefono`) VALUES
(1, 'Carlos', 'Pérez', 'carlosperez@example.com', '$2b$12$yH8WEl.eFgdO6PttTRx3gOxQ0oA1zUl81nlmlJwBX2/j0vWh0dpGm', 25, 'admin', 2, 71, 'Male', '555-1234'),
(2, 'Ana', 'Gómez', 'anagomez@example.com', '$2b$12$4F0mH1XlYzImEnlOkGyTtOHtD2jA4p9wOsfhj6wMj8rF/9a4.N1Ke', 30, 'usuario', 2, 65, 'Female', '555-5678'),
(3, 'Luis', 'Martínez', 'luismartinez@example.com', '$2b$12$Yb7o4CkDKgM1G6If2RjX7rB0y.rWI7cWxdQdZFSdMN6DAGzSZ.wEm', 22, 'admin', 2, 80, 'Male', '555-9876'),
(4, 'Lucía', 'Hernández', 'luciahernandez@example.com', '$2b$12$XNx1Gr0BkgZlLRAZ7J9w/7P.yNVlXUHpOZm6pXknzmnIwlAebjxX2', 28, 'usuario', 2, 55, 'Female', '555-1122'),
(5, 'Pedro', 'Rodríguez', 'pedrorodriguez@example.com', '$2b$12$DfiR0sHlXziK4d7g6HZtP1ld01yDx8vhFHJZb4i/ukPzxwYcHp4PC', 35, 'usuario', 2, 85, 'Male', '555-3344'),
(54, 'Fulano', 'De Tal', 'fulano@gmail.com', 'scrypt:32768:8:1$GUQbsBqvrCxKpdit$66a1236f81662a83679369396c49acc15f3e95b8d85aa364381be9e6807a1a8373d611f2383ab0a3d70eb9b2a2d21db974d5add167f2f92c7f1ccf1c800788d4', 34, 'admin', 183, 85, 'Male', '624578321');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `contacto`
--
ALTER TABLE `contacto`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `instalaciones`
--
ALTER TABLE `instalaciones`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `reservas`
--
ALTER TABLE `reservas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_instalacion` (`id_instalacion`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `contacto`
--
ALTER TABLE `contacto`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `instalaciones`
--
ALTER TABLE `instalaciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `reservas`
--
ALTER TABLE `reservas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=55;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `reservas`
--
ALTER TABLE `reservas`
  ADD CONSTRAINT `reservas_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `reservas_ibfk_2` FOREIGN KEY (`id_instalacion`) REFERENCES `instalaciones` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
