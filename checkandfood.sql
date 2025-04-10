-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: checkandfood
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `customer_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone_number` varchar(25) NOT NULL,
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (8,'Jorge','jorge@gmail.com','scrypt:32768:8:1$7pS4MW5uPxzbKmHW$8f9f2b1942057444d99915e54b1623d38b4cf0c6d12e82c76a947e46d0e551e88491e81fa82c31423ce4eb19e55f2edf09cb2201f829bd0fc6903b2af2be1456','500521523');
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `food`
--

DROP TABLE IF EXISTS `food`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `food` (
  `food_id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(255) NOT NULL,
  PRIMARY KEY (`food_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `food`
--

LOCK TABLES `food` WRITE;
/*!40000 ALTER TABLE `food` DISABLE KEYS */;
INSERT INTO `food` VALUES (1,'Mediterranea'),(2,'Española'),(3,'Italiana'),(4,'Japonesa'),(5,'Mexicana'),(6,'Francesa'),(7,'China'),(8,'India'),(9,'Argentina'),(10,'Tailandesa'),(11,'Americana'),(12,'Vegana'),(13,'Coreana'),(14,'Griega'),(15,'Peruana'),(16,'Otras');
/*!40000 ALTER TABLE `food` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reserve`
--

DROP TABLE IF EXISTS `reserve`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reserve` (
  `reserve_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` int(11) NOT NULL,
  `time_slot_id` int(11) NOT NULL,
  `number_of_people` int(4) NOT NULL,
  `reserve_time` date NOT NULL,
  `estatus` enum('pendiente','aceptada','rechazada','cancelada') DEFAULT 'pendiente',
  `restaurant_id` int(11) NOT NULL,
  PRIMARY KEY (`reserve_id`),
  KEY `customer_id` (`customer_id`),
  KEY `time_slot_id` (`time_slot_id`),
  CONSTRAINT `reserve_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `reserve_ibfk_3` FOREIGN KEY (`time_slot_id`) REFERENCES `time_slot` (`time_slot_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reserve`
--

LOCK TABLES `reserve` WRITE;
/*!40000 ALTER TABLE `reserve` DISABLE KEYS */;
INSERT INTO `reserve` VALUES (15,8,50,4,'2025-04-04','cancelada',17),(16,8,55,2,'2025-04-06','cancelada',18),(17,8,71,4,'2025-04-05','cancelada',21),(18,8,73,3,'2025-04-04','rechazada',21),(19,8,45,2,'2025-04-25','aceptada',17),(20,8,45,2,'2025-04-10','pendiente',17),(21,8,87,4,'2025-04-06','aceptada',23);
/*!40000 ALTER TABLE `reserve` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `restaurant`
--

DROP TABLE IF EXISTS `restaurant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `restaurant` (
  `restaurant_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `password` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `capacity` int(4) NOT NULL,
  `phone_number` varchar(14) NOT NULL,
  `description` tinytext DEFAULT NULL,
  `speciality` tinytext DEFAULT NULL,
  `web` varchar(255) DEFAULT NULL,
  `img_url` varchar(255) DEFAULT NULL,
  `food_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`restaurant_id`),
  UNIQUE KEY `username_UNIQUE` (`email`),
  KEY `food_id` (`food_id`),
  CONSTRAINT `restaurant_ibfk_1` FOREIGN KEY (`food_id`) REFERENCES `food` (`food_id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `restaurant`
--

LOCK TABLES `restaurant` WRITE;
/*!40000 ALTER TABLE `restaurant` DISABLE KEYS */;
INSERT INTO `restaurant` VALUES (17,'El Olivo Dorado','elolivodorado@gmail.com','scrypt:32768:8:1$VXZPbSbEHgbT0ag4$8cc9c3c0530c36ad8da8fe89d5b25b6f3ad2398661fc9cfef8c07b5007631be47e26cd0101de3fbc5a80ade47dcbc85d08f5dff312ec2adfbc206636d21e830b','Rúa do Príncipe 123, Vigo, España',25,'+34 986 456 78','Un rincón acogedor en el corazón de Vigo, famoso por su paella de mariscos y tapas tradicionales.','Paella de mariscos y pulpo a la gallega.',' www.elolivodorado.com','El_olivo_dorado.jpeg',1),(18,'La Brisa Azul','labrisaazul@gmail.com','scrypt:32768:8:1$0NIOsEWD6tTNwC0c$cccac3f995848f41c2f4b3485bb5e92b39789255580455b20fb51533f5b54ac027ac2d0d1055e074d6cde36015155f44c873de27da7af888d47ad0a3db318835','Avenida Samil 45, Vigo, España',30,'+34 986 234 56','Un restaurante con vistas a la Ría de Vigo, especializado en pescados frescos y ensaladas saludables.','Lubina a la sal y ensalada griega.',' www.labrisaazul.com','la_brisa_azul.png',1),(19,'Terra & Mar','terra&mar@gmail.com','scrypt:32768:8:1$JZvwnNHZAidpoDYY$f37f9372b9720ea5a8645723d9c3e4ac7ea21b60658fa151c26a7e7c1b3eab8031f663a7b9486779dc57af1108e7c96c7f0f5b7409b2fa3e3539b51f62a07094','Praza da Constitución 8, Vigo, España',20,'+34 986 789 45','Un elegante restaurante que fusiona lo mejor del mar y la tierra con ingredientes frescos de la región.','Risotto de mariscos y carpaccio de atún.',' www.terramar.es','terramar.png',1),(20,'Sirocco Taverna','siroccotaverna@gmail.com','scrypt:32768:8:1$hw5hhzsqLrxVx1RS$de8e4ef0fe23d0d83ea652b8c625c1fa736238c0b2f7a6c53e328c5617e6e98a32405dae55284501fb6808c72817b41d77a8454231f9b7031566afc67df63e10','Rúa da Ostrería 22, Vigo, España',25,'+34 986 987 65','Una taberna mediterránea con un ambiente cálido, perfecta para disfrutar de auténticas mezedes y vinos locales.','Moussaka y souvlaki de cordero.','www.siroccotaverna.es','siroco_taverna.png',1),(21,'Costa del Sabor','costadelsabor@gmail.com','scrypt:32768:8:1$J4RYE29UKFZmBp8n$702930b289b83db16343decac11e42aad546fb0f802b1602266b9ee201fc73bcc3d9f2e278cf23e6b05242269f53d8d99c764daa6b227f8a8a47f29943220ba2','Paseo de Alfonso XII 77, Vigo, España',18,'+34 986 321 78','Un lugar ideal para disfrutar de la auténtica comida gallega con un toque mediterráneo y vistas a la ría.','Gazpacho andaluz y boquerones en vinagre.',' www.costadelsabor.com','Costa_del_Sabor.jpeg',1),(22,'La Bodega del Puerto','labodegadelpuerto@gmail.com','scrypt:32768:8:1$XQ9qOYT0ERxGMdm5$f031044113b0eb6e857f17caf2b08995ec47f03b4b0ddcd6b0f57cd7ab3f5e03b5e1086e613d2638c5d9f1d95767fc077077434ff3916858efbfbaed704fda5a','Calle del Arenal, 15, 36201 Vigo',20,'986 12 34 56','Un acogedor restaurante con una amplia selección de vinos españoles y tapas tradicionales.','Marisco y Paella.','www.labodegadelpuertovigo.com','bodegapuerto.png',2),(23,'El Rincón de Galicia','elrincondegalicia@gmail.com','scrypt:32768:8:1$blQIisWTENEGr6pv$85d733dfb4a3ea641057c8275fa6af06528a445821f2bdbfe9715e00212598be4d0429f37d8e3f05edf21df3c5e276b53b59c4763ca08f4127e458208f2fca53','Plaza de Compostela, 8, 36202 Vigo',20,'986 65 43 21','Un restaurante familiar que ofrece platos gallegos auténticos con un toque moderno. ','Pulpo a la Gallega y Carnes a la Brasa.','www.elrincondegavigo.es','rincongalicia.png',2),(24,'Casa de Tapas Don Pepe','casadetapasdonpepe@gmail.com','scrypt:32768:8:1$vJDyHYY7abk803dI$a6036a8542053e24d34f4ac22446de96b540a0903e3c25b08598bd0c359821344fc4cc9f24c6f71fd3bf20090f47ce4ab144dd2ddfcbacba4c353f232ccf8ea8','Calle Príncipe, 22, 36202 Vigo.',30,'986 98 76 54','Un lugar animado y bullicioso donde se pueden degustar una gran variedad de tapas españolas.','Croquetas y Tortilla Española.','www.casadetapasdonpepe.es','tapasdonpepe.png',2),(25,'El Mesón Castellano','elmesoncastellano@gmail.com','scrypt:32768:8:1$zXj60eBMjcHwILWg$72602f0414ee83ac1171db06dfc4e2d8699c277a1a07772cd0df7b3859352e127e1ef857046da752d65eed9a4c09c0523e9f104517c312ab783b92c99e415ca3','Calle Colón, 5, 36201 Vigo.',50,'986 45 67 89','Un restaurante elegante que ofrece platos de la cocina castellana con una presentación cuidada. ','Cochinillo y Cordero.',' www.elmesoncastellano.com','mesoncastellano.png',2),(26,'La Paella de la Abuela','lapaelladelaabuela@gmail.com','scrypt:32768:8:1$5jUKCmfdXFsT70pj$83e1cea197fd92eb8485300aaa99bff0ff899119885fc43675569e6425a6c7d33aa93c99187dc593ab22f781e83b77fa9de20b37b15ff04d05abe9fbddf97e8d','Calle Rosalía de Castro, 10, 36202 Vigo.',30,'986 78 90 12','Un restaurante especializado en paellas y arroces, con recetas tradicionales transmitidas de generación en generación. Ambiente acogedor y familiar.','Paellas y Arroces.',' www.lapaelladelaabuela.com.','paellaabuela.png',2);
/*!40000 ALTER TABLE `restaurant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `time_slot`
--

DROP TABLE IF EXISTS `time_slot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `time_slot` (
  `time_slot_id` int(11) NOT NULL AUTO_INCREMENT,
  `restaurant_id` int(11) NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `reserve_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`time_slot_id`),
  KEY `restaurant_id` (`restaurant_id`),
  KEY `fk_reserva` (`reserve_id`),
  CONSTRAINT `fk_reserva` FOREIGN KEY (`reserve_id`) REFERENCES `reserve` (`reserve_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=108 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `time_slot`
--

LOCK TABLES `time_slot` WRITE;
/*!40000 ALTER TABLE `time_slot` DISABLE KEYS */;
INSERT INTO `time_slot` VALUES (38,16,'12:00:00','13:00:00',NULL),(39,16,'13:00:00','14:00:00',NULL),(40,16,'14:00:00','15:00:00',NULL),(41,16,'15:00:00','16:00:00',NULL),(42,16,'20:00:00','21:00:00',NULL),(43,16,'21:00:00','22:00:00',NULL),(44,16,'22:00:00','23:00:00',NULL),(45,17,'13:00:00','14:00:00',NULL),(46,17,'14:00:00','15:00:00',NULL),(47,17,'15:00:00','16:00:00',NULL),(48,17,'20:00:00','21:00:00',NULL),(49,17,'21:00:00','22:00:00',NULL),(50,17,'22:00:00','23:00:00',NULL),(51,18,'12:30:00','13:30:00',NULL),(52,18,'13:30:00','14:30:00',NULL),(53,18,'14:30:00','15:30:00',NULL),(54,18,'15:30:00','16:30:00',NULL),(55,18,'20:00:00','21:00:00',NULL),(56,18,'21:00:00','22:00:00',NULL),(57,18,'22:00:00','23:00:00',NULL),(58,19,'13:00:00','14:00:00',NULL),(59,19,'14:00:00','15:00:00',NULL),(60,19,'15:00:00','16:00:00',NULL),(61,19,'20:30:00','21:30:00',NULL),(62,19,'21:30:00','22:30:00',NULL),(63,19,'22:30:00','23:30:00',NULL),(64,20,'12:00:00','13:00:00',NULL),(65,20,'13:00:00','14:00:00',NULL),(66,20,'14:00:00','15:00:00',NULL),(67,20,'15:00:00','16:00:00',NULL),(68,20,'20:00:00','21:00:00',NULL),(69,20,'21:00:00','22:00:00',NULL),(70,20,'22:00:00','23:00:00',NULL),(71,21,'13:00:00','14:00:00',NULL),(72,21,'14:00:00','15:00:00',NULL),(73,21,'15:00:00','16:00:00',NULL),(74,21,'20:00:00','21:00:00',NULL),(75,21,'21:00:00','22:00:00',NULL),(76,21,'22:00:00','23:00:00',NULL),(77,22,'13:00:00','14:00:00',NULL),(78,22,'14:00:00','15:00:00',NULL),(79,22,'15:00:00','16:00:00',NULL),(80,22,'20:00:00','21:00:00',NULL),(81,22,'21:00:00','22:00:00',NULL),(82,22,'22:00:00','23:00:00',NULL),(83,23,'13:30:00','14:30:00',NULL),(84,23,'14:30:00','15:30:00',NULL),(85,23,'15:30:00','16:30:00',NULL),(86,23,'21:00:00','22:00:00',NULL),(87,23,'22:00:00','23:00:00',NULL),(88,23,'23:00:00','00:00:00',NULL),(89,24,'12:00:00','13:00:00',NULL),(90,24,'13:00:00','14:00:00',NULL),(91,24,'14:00:00','15:00:00',NULL),(92,24,'20:30:00','21:30:00',NULL),(93,24,'21:30:00','22:30:00',NULL),(94,24,'22:30:00','23:30:00',NULL),(95,25,'13:00:00','14:00:00',NULL),(96,25,'14:00:00','15:00:00',NULL),(97,25,'15:00:00','16:00:00',NULL),(98,25,'21:00:00','22:00:00',NULL),(99,25,'22:00:00','23:00:00',NULL),(100,25,'23:00:00','00:00:00',NULL),(101,26,'12:30:00','13:30:00',NULL),(102,26,'13:30:00','14:30:00',NULL),(103,26,'14:30:00','15:30:00',NULL),(104,26,'15:30:00','16:30:00',NULL),(105,26,'21:00:00','22:00:00',NULL),(106,26,'22:00:00','23:00:00',NULL),(107,26,'23:00:00','00:00:00',NULL);
/*!40000 ALTER TABLE `time_slot` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-11  0:15:48
