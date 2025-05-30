-- MySQL dump 10.13  Distrib 8.0.40, for Linux (x86_64)
--
-- Host: localhost    Database: mysqlRDS_littlelemon
-- ------------------------------------------------------
-- Server version	8.0.40-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `LittleLemonAPI_cart`
--

DROP TABLE IF EXISTS `LittleLemonAPI_cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LittleLemonAPI_cart` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` smallint NOT NULL,
  `unit_price` decimal(6,2) NOT NULL,
  `price` decimal(6,2) NOT NULL,
  `user_id` int NOT NULL,
  `menuitem_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `LittleLemonAPI_cart_menuitem_id_user_id_ecd9e087_uniq` (`menuitem_id`,`user_id`),
  KEY `LittleLemonAPI_cart_user_id_1689ef2e_fk_auth_user_id` (`user_id`),
  CONSTRAINT `LittleLemonAPI_cart_menuitem_id_d5ce9edb_fk_LittleLem` FOREIGN KEY (`menuitem_id`) REFERENCES `LittleLemonAPI_menuitem` (`id`),
  CONSTRAINT `LittleLemonAPI_cart_user_id_1689ef2e_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LittleLemonAPI_cart`
--

LOCK TABLES `LittleLemonAPI_cart` WRITE;
/*!40000 ALTER TABLE `LittleLemonAPI_cart` DISABLE KEYS */;
/*!40000 ALTER TABLE `LittleLemonAPI_cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `LittleLemonAPI_category`
--

DROP TABLE IF EXISTS `LittleLemonAPI_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LittleLemonAPI_category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `slug` varchar(50) NOT NULL,
  `title` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  KEY `LittleLemonAPI_category_title_71923fa6` (`title`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LittleLemonAPI_category`
--

LOCK TABLES `LittleLemonAPI_category` WRITE;
/*!40000 ALTER TABLE `LittleLemonAPI_category` DISABLE KEYS */;
INSERT INTO `LittleLemonAPI_category` VALUES (1,'drinks','Drinks'),(2,'meals','Meals'),(3,'desserts','Desserts'),(5,'appetizers','Appetizers');
/*!40000 ALTER TABLE `LittleLemonAPI_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `LittleLemonAPI_menuitem`
--

DROP TABLE IF EXISTS `LittleLemonAPI_menuitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LittleLemonAPI_menuitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `price` decimal(6,2) NOT NULL,
  `featured` tinyint(1) NOT NULL,
  `category_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `LittleLemonAPI_menui_category_id_d2a381bd_fk_LittleLem` (`category_id`),
  KEY `LittleLemonAPI_menuitem_title_d8d6f638` (`title`),
  KEY `LittleLemonAPI_menuitem_price_a4578e46` (`price`),
  KEY `LittleLemonAPI_menuitem_featured_40218f42` (`featured`),
  CONSTRAINT `LittleLemonAPI_menui_category_id_d2a381bd_fk_LittleLem` FOREIGN KEY (`category_id`) REFERENCES `LittleLemonAPI_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LittleLemonAPI_menuitem`
--

LOCK TABLES `LittleLemonAPI_menuitem` WRITE;
/*!40000 ALTER TABLE `LittleLemonAPI_menuitem` DISABLE KEYS */;
INSERT INTO `LittleLemonAPI_menuitem` VALUES (1,'Eggplant Parmiggiana',15.50,0,5),(2,'Soda',5.50,0,1),(3,'Crème Brûlée',7.25,0,3),(4,'Bruschetta',11.52,0,5),(5,'Canada Dry',4.78,0,1),(6,'Bolognese Lasagna',14.99,1,2);
/*!40000 ALTER TABLE `LittleLemonAPI_menuitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `LittleLemonAPI_order`
--

DROP TABLE IF EXISTS `LittleLemonAPI_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LittleLemonAPI_order` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` tinyint(1) NOT NULL,
  `total` decimal(6,2) NOT NULL,
  `date` date NOT NULL,
  `delivery_crew_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `LittleLemonAPI_order_delivery_crew_id_99a5a2c8_fk_auth_user_id` (`delivery_crew_id`),
  KEY `LittleLemonAPI_order_user_id_82eb7f1d_fk_auth_user_id` (`user_id`),
  KEY `LittleLemonAPI_order_status_7b5350c7` (`status`),
  KEY `LittleLemonAPI_order_date_f8faabe7` (`date`),
  CONSTRAINT `LittleLemonAPI_order_delivery_crew_id_99a5a2c8_fk_auth_user_id` FOREIGN KEY (`delivery_crew_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `LittleLemonAPI_order_user_id_82eb7f1d_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LittleLemonAPI_order`
--

LOCK TABLES `LittleLemonAPI_order` WRITE;
/*!40000 ALTER TABLE `LittleLemonAPI_order` DISABLE KEYS */;
/*!40000 ALTER TABLE `LittleLemonAPI_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `LittleLemonAPI_orderitem`
--

DROP TABLE IF EXISTS `LittleLemonAPI_orderitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LittleLemonAPI_orderitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` smallint NOT NULL,
  `unit_price` decimal(6,2) NOT NULL,
  `price` decimal(6,2) NOT NULL,
  `menuitem_id` bigint NOT NULL,
  `order_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `LittleLemonAPI_orderitem_order_id_menuitem_id_d9cdbc99_uniq` (`order_id`,`menuitem_id`),
  KEY `LittleLemonAPI_order_menuitem_id_87f2c784_fk_LittleLem` (`menuitem_id`),
  CONSTRAINT `LittleLemonAPI_order_menuitem_id_87f2c784_fk_LittleLem` FOREIGN KEY (`menuitem_id`) REFERENCES `LittleLemonAPI_menuitem` (`id`),
  CONSTRAINT `LittleLemonAPI_order_order_id_4169f7c4_fk_LittleLem` FOREIGN KEY (`order_id`) REFERENCES `LittleLemonAPI_order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LittleLemonAPI_orderitem`
--

LOCK TABLES `LittleLemonAPI_orderitem` WRITE;
/*!40000 ALTER TABLE `LittleLemonAPI_orderitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `LittleLemonAPI_orderitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (2,'delivery-crew'),(1,'Manager');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (3,1,10),(5,1,12),(8,1,16),(9,1,28),(10,1,29),(11,1,30),(12,1,31),(1,1,32),(2,1,41),(4,1,42),(6,1,43),(7,1,44),(13,2,40),(14,2,42);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add category',7,'add_category'),(26,'Can change category',7,'change_category'),(27,'Can delete category',7,'delete_category'),(28,'Can view category',7,'view_category'),(29,'Can add menu item',8,'add_menuitem'),(30,'Can change menu item',8,'change_menuitem'),(31,'Can delete menu item',8,'delete_menuitem'),(32,'Can view menu item',8,'view_menuitem'),(33,'Can add cart',9,'add_cart'),(34,'Can change cart',9,'change_cart'),(35,'Can delete cart',9,'delete_cart'),(36,'Can view cart',9,'view_cart'),(37,'Can add order',10,'add_order'),(38,'Can change order',10,'change_order'),(39,'Can delete order',10,'delete_order'),(40,'Can view order',10,'view_order'),(41,'Can add order item',11,'add_orderitem'),(42,'Can change order item',11,'change_orderitem'),(43,'Can delete order item',11,'delete_orderitem'),(44,'Can view order item',11,'view_orderitem'),(45,'Can add Token',12,'add_token'),(46,'Can change Token',12,'change_token'),(47,'Can delete Token',12,'delete_token'),(48,'Can view Token',12,'view_token'),(49,'Can add Token',13,'add_tokenproxy'),(50,'Can change Token',13,'change_tokenproxy'),(51,'Can delete Token',13,'delete_tokenproxy'),(52,'Can view Token',13,'view_tokenproxy');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (2,'pbkdf2_sha256$870000$VbNaWjSwTtfndYwY4Io90X$maT0bXqFtaNUniVYsDS2sAiJMbavJZjl5v7/TaDTcD0=','2025-01-17 14:04:46.219621',1,'Super2025','','','',1,1,'2025-01-17 14:02:20.407735');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-01-17 14:05:52.555280','1','Drinks',1,'[{\"added\": {}}]',7,2),(2,'2025-01-17 14:06:04.218354','2','Meals',1,'[{\"added\": {}}]',7,2),(3,'2025-01-17 14:06:15.805388','3','Desserts',1,'[{\"added\": {}}]',7,2),(4,'2025-01-17 14:06:56.788452','4','Entries',1,'[{\"added\": {}}]',7,2),(5,'2025-01-17 14:08:00.051343','4','Entries',3,'',7,2),(6,'2025-01-17 14:08:14.587231','5','Appetizers',1,'[{\"added\": {}}]',7,2),(7,'2025-01-17 14:08:45.820905','1','Eggplant Parmiggiana',1,'[{\"added\": {}}]',8,2),(8,'2025-01-17 14:08:58.515634','2','Soda',1,'[{\"added\": {}}]',8,2),(9,'2025-01-17 14:10:00.805504','3','Crème Brûlée',1,'[{\"added\": {}}]',8,2),(10,'2025-01-17 14:10:43.955574','4','Bruschetta',1,'[{\"added\": {}}]',8,2),(11,'2025-01-17 14:11:07.229359','5','Canada Dry',1,'[{\"added\": {}}]',8,2),(12,'2025-01-17 14:12:45.250698','6','Bolognese Lasagna',1,'[{\"added\": {}}]',8,2),(13,'2025-01-17 14:24:56.290822','1','Manager',1,'[{\"added\": {}}]',3,2),(14,'2025-01-17 14:26:37.985392','2','delivery-crew',1,'[{\"added\": {}}]',3,2),(15,'2025-01-17 14:27:23.372273','1','Super',3,'',4,2);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(12,'authtoken','token'),(13,'authtoken','tokenproxy'),(5,'contenttypes','contenttype'),(9,'LittleLemonAPI','cart'),(7,'LittleLemonAPI','category'),(8,'LittleLemonAPI','menuitem'),(10,'LittleLemonAPI','order'),(11,'LittleLemonAPI','orderitem'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-01-17 00:44:37.499162'),(2,'auth','0001_initial','2025-01-17 00:44:37.975339'),(3,'admin','0001_initial','2025-01-17 00:44:38.101292'),(4,'admin','0002_logentry_remove_auto_add','2025-01-17 00:44:38.116516'),(5,'admin','0003_logentry_add_action_flag_choices','2025-01-17 00:44:38.136307'),(6,'contenttypes','0002_remove_content_type_name','2025-01-17 00:44:38.254426'),(7,'auth','0002_alter_permission_name_max_length','2025-01-17 00:44:38.325597'),(8,'auth','0003_alter_user_email_max_length','2025-01-17 00:44:38.372656'),(9,'auth','0004_alter_user_username_opts','2025-01-17 00:44:38.393768'),(10,'auth','0005_alter_user_last_login_null','2025-01-17 00:44:38.465465'),(11,'auth','0006_require_contenttypes_0002','2025-01-17 00:44:38.468637'),(12,'auth','0007_alter_validators_add_error_messages','2025-01-17 00:44:38.491215'),(13,'auth','0008_alter_user_username_max_length','2025-01-17 00:44:38.566413'),(14,'auth','0009_alter_user_last_name_max_length','2025-01-17 00:44:38.636853'),(15,'auth','0010_alter_group_name_max_length','2025-01-17 00:44:38.688458'),(16,'auth','0011_update_proxy_permissions','2025-01-17 00:44:38.713588'),(17,'auth','0012_alter_user_first_name_max_length','2025-01-17 00:44:38.792155'),(18,'authtoken','0001_initial','2025-01-17 00:44:38.861258'),(19,'authtoken','0002_auto_20160226_1747','2025-01-17 00:44:38.921488'),(20,'authtoken','0003_tokenproxy','2025-01-17 00:44:38.925840'),(21,'authtoken','0004_alter_tokenproxy_options','2025-01-17 00:44:38.935613'),(22,'sessions','0001_initial','2025-01-17 00:44:38.979099'),(23,'LittleLemonAPI','0001_initial','2025-01-17 00:45:27.939203');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('0fim1319mvhamzuxpzhkv57m0ez1ddjo','.eJxVjDkOwjAURO_iGlnewZT0OYP1FxsHkCPFSYW4O4mUAsqZ92beIsG61LT2PKeRxVUYcfrtEOiZ2w74Ae0-SZraMo8od0UetMth4vy6He7fQYVet7UvrJBtNgqdQh1KiR40WXCuYA6BthitYbTGKa1K8Bcma84RWRMCiM8X94A4cw:1tYmxq:QvCgQPd3sfWsikMFU34EOYR-h0Lox2NdECyU7AzZJu0','2025-01-31 14:04:46.225311');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-17  9:31:05
