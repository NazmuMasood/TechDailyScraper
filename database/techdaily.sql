-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 18, 2021 at 10:28 PM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 8.0.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `techdaily`
--

-- --------------------------------------------------------

--
-- Table structure for table `techdaily_content`
--

CREATE TABLE `techdaily_content` (
  `id` bigint(20) NOT NULL,
  `url` varchar(300) NOT NULL,
  `title` varchar(200) NOT NULL,
  `author` varchar(40) DEFAULT NULL,
  `pub_date` varchar(50) DEFAULT NULL,
  `img_url` varchar(500) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  `owner_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `techdaily_owner`
--

CREATE TABLE `techdaily_owner` (
  `id` bigint(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `url` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `techdaily_owner`
--

INSERT INTO `techdaily_owner` (`id`, `name`, `url`, `created_at`, `updated_at`) VALUES
(1, 'Cnet', 'https://www.cnet.com', '2021-06-18 23:51:46.000000', NULL),
(2, 'Beebom', 'https://beebom.com/', '2021-06-18 23:51:46.000000', NULL),
(3, 'Android Authority', 'https://www.androidauthority.com/news/', '2021-06-18 23:51:46.000000', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `techdaily_content`
--
ALTER TABLE `techdaily_content`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `url` (`url`),
  ADD KEY `techdaily_content_owner_id_f4bd664e_fk_techdaily_owner_id` (`owner_id`);

--
-- Indexes for table `techdaily_owner`
--
ALTER TABLE `techdaily_owner`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `url` (`url`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `techdaily_content`
--
ALTER TABLE `techdaily_content`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT for table `techdaily_owner`
--
ALTER TABLE `techdaily_owner`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `techdaily_content`
--
ALTER TABLE `techdaily_content`
  ADD CONSTRAINT `techdaily_content_owner_id_f4bd664e_fk_techdaily_owner_id` FOREIGN KEY (`owner_id`) REFERENCES `techdaily_owner` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
