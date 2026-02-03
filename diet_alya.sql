-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 03 Feb 2026 pada 03.47
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `diet_alya`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `tb_catatan_makanan`
--

CREATE TABLE `tb_catatan_makanan` (
  `id_catatan` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `id_makanan` int(11) NOT NULL,
  `waktu_makan` enum('pagi','siang','sore') NOT NULL,
  `jml_porsi` decimal(5,2) NOT NULL,
  `tgl` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `tb_catatan_olahraga`
--

CREATE TABLE `tb_catatan_olahraga` (
  `id_catatan` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `id_olahraga` int(11) NOT NULL,
  `durasi_menit` int(11) NOT NULL,
  `kalori_terbakar` int(11) NOT NULL,
  `tgl` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `tb_food`
--

CREATE TABLE `tb_food` (
  `id_makanan` int(11) NOT NULL,
  `nama_makanan` varchar(150) NOT NULL,
  `kalori` int(11) NOT NULL,
  `protein` decimal(5,2) NOT NULL,
  `lemak` decimal(5,2) NOT NULL,
  `karbo` decimal(5,2) NOT NULL,
  `porsi` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `tb_olahraga`
--

CREATE TABLE `tb_olahraga` (
  `id_olahraga` int(11) NOT NULL,
  `nama_olahraga` varchar(100) NOT NULL,
  `kalori_per_menit` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `tb_user`
--

CREATE TABLE `tb_user` (
  `id_user` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `email` int(100) NOT NULL,
  `password` int(255) NOT NULL,
  `gender` enum('pria','wanita') NOT NULL,
  `tgl_lahir` date NOT NULL,
  `tinggi_badan` int(2) NOT NULL,
  `berat_badan` decimal(5,2) NOT NULL,
  `tingkat_aktivitas` enum('rendah','sedang','tinggi') NOT NULL,
  `tujuan` enum('diet','jaga','naik') NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `user_targets`
--

CREATE TABLE `user_targets` (
  `id_targets` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `target_kalori` int(11) NOT NULL,
  `target_protein` int(11) NOT NULL,
  `target_lemak` int(11) NOT NULL,
  `target_karbo` int(11) NOT NULL,
  `updated_at` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `tb_catatan_olahraga`
--
ALTER TABLE `tb_catatan_olahraga`
  ADD PRIMARY KEY (`id_catatan`);

--
-- Indeks untuk tabel `tb_food`
--
ALTER TABLE `tb_food`
  ADD PRIMARY KEY (`id_makanan`);

--
-- Indeks untuk tabel `tb_olahraga`
--
ALTER TABLE `tb_olahraga`
  ADD PRIMARY KEY (`id_olahraga`);

--
-- Indeks untuk tabel `tb_user`
--
ALTER TABLE `tb_user`
  ADD PRIMARY KEY (`id_user`),
  ADD KEY `email` (`email`);

--
-- Indeks untuk tabel `user_targets`
--
ALTER TABLE `user_targets`
  ADD PRIMARY KEY (`id_targets`),
  ADD UNIQUE KEY `id_user` (`id_user`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
