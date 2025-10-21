-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:5000
-- Server version: 5.7.21
-- PHP Version: 7.3.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

#-*-coding:utf-8*-

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- VeriTabanı: `mekaya`
--

-- --------------------------------------------------------

--
--  `admin` tablosu için dumping verileri
--

DROP TABLE IF EXISTS `admin`;
CREATE TABLE IF NOT EXISTS `admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `firstName` varchar(125) NOT NULL,
  `lastName` varchar(125) NOT NULL,
  `email` varchar(100) NOT NULL,
  `mobile` varchar(25) NOT NULL,
  `address` text NOT NULL,
  `password` varchar(100) NOT NULL,
  `type` varchar(20) NOT NULL,
  `confirmCode` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4_turkish_ci;

--
--  `admin` tablosu için dumping verileri
--

INSERT INTO `admin` (`id`, `firstName`, `lastName`, `email`, `mobile`, `address`, `password`, `type`, `confirmCode`) VALUES
(1, 'Murat Elber ', 'Kaya', 'elberfener@gmail.com', '05532258355', 'İstanbul', '$5$rounds=535000$WOAOMdgoK2JpZLY5$RFH9BZQCB3NEvG4R/FofxxJL/PUaeZm7T6G9P3PRg05', 'manager', '0');

-- --------------------------------------------------------

--
--  `orders` tablosu için dumping verileri
--

DROP TABLE IF EXISTS `orders`;
CREATE TABLE IF NOT EXISTS `orders` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) DEFAULT NULL,
  `ofname` text NOT NULL,
  `pid` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `oplace` text NOT NULL,
  `mobile` varchar(15) NOT NULL,
  `dstatus` varchar(10) NOT NULL DEFAULT 'no',
  `odate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ddate` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4_turkish_ci;
-- --------------------------------------------------------

--
-- `products` tablosu için dumping verileri
--

DROP TABLE IF EXISTS `products`;
CREATE TABLE IF NOT EXISTS `products` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pName` varchar(100) NOT NULL,
  `price` int(11) NOT NULL,
  `description` text NOT NULL,
  `available` int(11) NOT NULL,
  `category` varchar(100) NOT NULL,
  `item` varchar(100) NOT NULL,
  `pCode` varchar(20) NOT NULL,
  `picture` text NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4_turkish_ci;

--
--  `products` tablosu için dumping verileri
--

INSERT INTO `products` (`id`, `pName`, `price`, `description`, `available`, `category`, `item`, `pCode`, `picture`, `date`) VALUES
(1, 'Siyah Tişört', 30, 'Cepli Siyah tişört', 4, 'tshirt', 't-shirt', 't-007', '1dbfb5e8d1b8da1d3f36ee9b8bc19861.jpg', '2020-07-05 12:20:40'),
(2, 'Dolce&Gabbana Cüzdan', 2500, 'Yıldız baskılı, logolu,gerçek deri cüzdan. 6 adet kart bölmeli, 1 adet iç cepli', 3, 'wallet', 'wallet', 'w-004', 'dolce-gabbana-cuzdan.jpg', '2020-07-05 12:25:28'),
(3, 'Mokasen Ayakkabı', 175, 'Mokasen gerçek deri kahverengi ayakkabı', 8, 'shoes', 'shoes', 's-001', '8544789_5_.jpg', '2020-07-05 12:27:28'),
(4, 'Versace Kemer', 1500, 'Kahverengi renkli medusa tokalı gerçek deri kemer', 9, 'belt', 'belt', 'b-001', 'versace-erkek-kahverengi-medusa-tokali-deri-kemer-00-eu.jpg', '2020-07-05 12:29:46'),
(5, 'Polo Tişört', 80, 'Polo mavi renk tişört', 10, 'tshirt', 't-shirt', 's-002', 'lp00-2.jpg', '2020-07-05 12:35:24'),
(6, 'Polo Tişört', 80, 'Polo sarı renk tişört', 12, 'tshirt', 't-shirt', 't-003', 'yellow_2_.jpg', '2020-07-05 12:38:11'),
(7, 'Tasarım Tişört', 120, 'Özel tasarım kırmızı tişört', 10, 'tshirt', 't-shirt', 't-004', 'MSTSV14042.jpg', '2020-07-05 12:44:35'),
(8, 'Beyaz Tişört', 20, 'Düz beyaz tişört', 20, 'tshirt', 't-shirt', 't-005', 'MSTS14759.jpg', '2020-07-05 12:47:35'),
(9, 'COD Tasarım Tişört', 135, 'Call of Duty Modern Warfare oyununun özel tasarım tişörtü', 20, 'tshirt', 't-shirt', 't-006', '610ERXeGqkL._AC_UL1050_.jpg', '2020-07-05 12:48:52'),
(10, 'Milli Takım Tişört', 150, 'Lotto alev desenli milli takım tişörtü', 5, 'tshirt', 't-shirt', 't-007', '10219953717298.jpg', '2020-07-05 13:17:43'),
(12, 'Kaft Tasarım Tişört', 80, 'Kaft marka mavi renk özel tasarım tişört', 10, 'tshirt', 't-shirt', 't-010', '1000_1.jpg', '2020-07-05 13:19:17'),
(13, 'Kışlık Bot', 120, 'Yeşil bağcıklı suni deri bot', 10, 'shoes', 'shoes', 's-002', 'yesil-bagcikli-kislik-erkek-bot-postaleb-db51.jpg', '2020-07-05 13:22:25'),
(14, 'Versace Kristal 3D Kemer', 7500, 'Versace Siyah Deri Swarovski Kristal 3D Medusa Kemer', 20, 'belt', 'belt', 'b-003', '2504673_l.jpg', '2020-07-05 13:29:34'),
(15, 'Spor Süet Kemer', 50, 'Lacivert süet kemer', 20, 'belt', 'belt', 'b-004', 'fbd7fb0b-2c17-432b-982e-e8825b1a1fc3_size350x525_quality90_cropCenter.jpg', '2020-07-05 13:33:58'),
(16, 'Siyah Rugan Kemer', 100, 'Siyah klasik rugan deri kemer', 15, 'belt', 'belt', 'b-005', 'image4_2.jpg', '2020-07-05 13:36:08'),
(17, 'Baborry Cüzdan', 100, 'Baborry marka çift fermuarlı siyah gerçek deri cüzdan', 10, 'wallet', 'wallet', 'w-005', 'Baborry-Double-Zipper-Coin-Bag-RFID-Blocking-Men-Wallets-New-Brand-PU-Leather-Wallet-Money-Purses.jpg_640x640.jpg', '2020-07-05 13:38:15'),
(18, 'Kemal Tanca Cüzdan', 150, 'Kemal Tanca marka gri renkli gerçek deri cüzdan', 20, 'wallet', 'wallet', 'w-007', '03195ed3-4794-48c9-b1cc-1e56db3e977d_size780x780_cropCenter.jpg', '2020-07-05 13:41:29'),
(19, 'Siyah Cüzdan', 15, 'Siyah suni deri cüzdan', 20, 'wallet', 'wallet', 'w-009', 'indir.jpg', '2020-07-05 13:43:20'),
(20, 'Futbol Krampon Ayakkabı', 250, 'NİKE Mercurial Victory Vi ', 23, 'shoes', 'shoes', 's-003', 'nike-mercurial-victory-vi-df-fg-krampon-903609404-1.jpg', '2020-07-05 13:45:15'),
(21, 'Rugan Ayakkabı', 300, 'Klasik siyah rugan ayakkabı', 12, 'shoes', 'shoes', 's-004', '8f7ec067-2fed-4a27-a04f-f167631a97b4_size780x780_cropCenter.jpg', '2020-07-05 13:49:53');

-- --------------------------------------------------------

--
--  `product_level` tablosu için dumping verileri
--

DROP TABLE IF EXISTS `product_level`;
CREATE TABLE IF NOT EXISTS `product_level` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `v_shape` varchar(10) NOT NULL DEFAULT 'no',
  `polo` varchar(10) NOT NULL DEFAULT 'no',
  `clean_text` varchar(10) NOT NULL DEFAULT 'no',
  `design` varchar(10) NOT NULL DEFAULT 'no',
  `chain` varchar(10) NOT NULL DEFAULT 'no',
  `leather` varchar(10) NOT NULL DEFAULT 'no',
  `hook` varchar(10) NOT NULL DEFAULT 'no',
  `color` varchar(10) NOT NULL DEFAULT 'no',
  `formal` varchar(10) NOT NULL DEFAULT 'no',
  `converse` varchar(10) NOT NULL DEFAULT 'no',
  `loafer` varchar(10) NOT NULL DEFAULT 'no',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4_turkish_ci;

--
-- `product_level` tablosu için dumping verileri
--

INSERT INTO `product_level` (`id`, `product_id`, `v_shape`, `polo`, `clean_text`, `design`, `chain`, `leather`, `hook`, `color`, `resmi`, `converse`, `loafer`) VALUES
(1, 1, 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(2, 2, 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no'),
(3, 3, 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'yes'),
(4, 4, 'no', 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'no'),
(5, 5, 'no', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(6, 6, 'no', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(7, 7, 'yes', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(8, 8, 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(9, 9, 'yes', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(10, 10, 'yes', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(14, 14, 'no', 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'no'),
(12, 12, 'yes', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(13, 13, 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'yes'),
(15, 15, 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'yes', 'no', 'no', 'no'),
(16, 16, 'no', 'no', 'no', 'no', 'no', 'yes', 'yes', 'yes', 'no', 'no', 'no'),
(17, 17, 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no'),
(18, 18, 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no'),
(19, 19, 'no', 'no', 'no', 'yes', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no'),
(20, 20, 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no'),
(21, 21, 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'yes', 'no', 'no');

-- --------------------------------------------------------

--
--  `product_view` için tablo yapısı
--

DROP TABLE IF EXISTS `product_view`;
CREATE TABLE IF NOT EXISTS `product_view` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4_turkish_ci;

--
-- `product_view` tablosu için dumping verileri
--

INSERT INTO `product_view` (`id`, `user_id`, `product_id`, `date`) VALUES
(1, 9, 9, '2018-09-22 02:19:30'),
(2, 9, 7, '2018-09-27 02:47:43'),
(3, 9, 12, '2018-09-22 03:20:59'),
(4, 9, 10, '2018-09-29 03:07:11'),
(5, 9, 5, '2018-09-22 03:19:19'),
(6, 9, 8, '2018-09-21 15:57:50'),
(7, 9, 6, '2018-09-22 02:12:54'),
(8, 9, 1, '2018-09-22 03:03:36');

-- --------------------------------------------------------

--
-- TABLO YAPISI
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `username` varchar(25) NOT NULL,
  `password` varchar(100) NOT NULL,
  `mobile` varchar(20) NOT NULL,
  `reg_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `online` varchar(1) NOT NULL DEFAULT '0',
  `activation` varchar(3) NOT NULL DEFAULT 'yes',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4_turkish_ci;




/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
