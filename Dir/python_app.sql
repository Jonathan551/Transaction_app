-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 06, 2025 at 04:38 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `python_app`
--

-- --------------------------------------------------------

--
-- Table structure for table `fingerprint`
--

CREATE TABLE `fingerprint` (
  `id_fingerprint` int(11) NOT NULL,
  `id_user` int(11) DEFAULT NULL,
  `file_path` varchar(255) DEFAULT NULL,
  `template_hash` text DEFAULT NULL,
  `tanggal_upload` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `fingerprint`
--

INSERT INTO `fingerprint` (`id_fingerprint`, `id_user`, `file_path`, `template_hash`, `tanggal_upload`) VALUES
(3, 1, 'd:\\Tugas Kuliah\\Python App\\Dir\\fingerprints\\Joni.png', NULL, '2025-07-06 14:11:22');

-- --------------------------------------------------------

--
-- Table structure for table `request_topup`
--

CREATE TABLE `request_topup` (
  `id_request` int(11) NOT NULL,
  `id_user` int(11) DEFAULT NULL,
  `jumlah` decimal(15,2) NOT NULL,
  `status` enum('Pending','Approved','Rejected') DEFAULT 'Pending',
  `tanggal_request` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `request_topup`
--

INSERT INTO `request_topup` (`id_request`, `id_user`, `jumlah`, `status`, `tanggal_request`) VALUES
(1, 2, 150000.00, 'Rejected', '2025-07-04 15:38:41'),
(2, 2, 20000000.00, 'Approved', '2025-07-06 14:18:51'),
(3, 2, 20000000.00, 'Rejected', '2025-07-06 14:19:46'),
(4, 2, 15000.00, 'Approved', '2025-07-06 14:21:31');

-- --------------------------------------------------------

--
-- Table structure for table `role`
--

CREATE TABLE `role` (
  `id_role` int(11) NOT NULL,
  `nama_role` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `role`
--

INSERT INTO `role` (`id_role`, `nama_role`) VALUES
(1, 'Admin'),
(2, 'Customer'),
(3, 'Supervisor');

-- --------------------------------------------------------

--
-- Table structure for table `saldo`
--

CREATE TABLE `saldo` (
  `id_saldo` int(11) NOT NULL,
  `id_user` int(11) DEFAULT NULL,
  `saldo` decimal(15,2) DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `saldo`
--

INSERT INTO `saldo` (`id_saldo`, `id_user`, `saldo`) VALUES
(1, 2, 20085000.00);

-- --------------------------------------------------------

--
-- Table structure for table `transaksi`
--

CREATE TABLE `transaksi` (
  `id_transaksi` int(11) NOT NULL,
  `id_pengirim` int(11) DEFAULT NULL,
  `id_penerima` int(11) DEFAULT NULL,
  `jumlah` decimal(15,2) NOT NULL,
  `tanggal_transaksi` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id_user` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `id_role` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id_user`, `username`, `password`, `id_role`) VALUES
(1, 'Joni', '12345', 1),
(2, 'Gilbert', '12345', 2),
(3, 'Felix', '12345', 3),
(4, 'Albert', '12345', 2);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `fingerprint`
--
ALTER TABLE `fingerprint`
  ADD PRIMARY KEY (`id_fingerprint`),
  ADD KEY `id_user` (`id_user`);

--
-- Indexes for table `request_topup`
--
ALTER TABLE `request_topup`
  ADD PRIMARY KEY (`id_request`),
  ADD KEY `id_user` (`id_user`);

--
-- Indexes for table `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`id_role`),
  ADD UNIQUE KEY `nama_role` (`nama_role`);

--
-- Indexes for table `saldo`
--
ALTER TABLE `saldo`
  ADD PRIMARY KEY (`id_saldo`),
  ADD KEY `id_user` (`id_user`);

--
-- Indexes for table `transaksi`
--
ALTER TABLE `transaksi`
  ADD PRIMARY KEY (`id_transaksi`),
  ADD KEY `id_pengirim` (`id_pengirim`),
  ADD KEY `id_penerima` (`id_penerima`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id_user`),
  ADD UNIQUE KEY `username` (`username`),
  ADD KEY `id_role` (`id_role`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `fingerprint`
--
ALTER TABLE `fingerprint`
  MODIFY `id_fingerprint` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `request_topup`
--
ALTER TABLE `request_topup`
  MODIFY `id_request` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `role`
--
ALTER TABLE `role`
  MODIFY `id_role` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `saldo`
--
ALTER TABLE `saldo`
  MODIFY `id_saldo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `transaksi`
--
ALTER TABLE `transaksi`
  MODIFY `id_transaksi` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `fingerprint`
--
ALTER TABLE `fingerprint`
  ADD CONSTRAINT `fingerprint_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`);

--
-- Constraints for table `request_topup`
--
ALTER TABLE `request_topup`
  ADD CONSTRAINT `request_topup_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`);

--
-- Constraints for table `saldo`
--
ALTER TABLE `saldo`
  ADD CONSTRAINT `saldo_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`);

--
-- Constraints for table `transaksi`
--
ALTER TABLE `transaksi`
  ADD CONSTRAINT `transaksi_ibfk_1` FOREIGN KEY (`id_pengirim`) REFERENCES `saldo` (`id_saldo`),
  ADD CONSTRAINT `transaksi_ibfk_2` FOREIGN KEY (`id_penerima`) REFERENCES `saldo` (`id_saldo`);

--
-- Constraints for table `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `user_ibfk_1` FOREIGN KEY (`id_role`) REFERENCES `role` (`id_role`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
