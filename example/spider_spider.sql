-- MySQL dump 10.13  Distrib 5.7.17, for Linux (x86_64)
--
-- Host: localhost    Database: spider
-- ------------------------------------------------------
-- Server version	5.7.17-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `spider`
--

DROP TABLE IF EXISTS `spider`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spider` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `url` varchar(256) NOT NULL,
  `urlstag` varchar(255) NOT NULL,
  `restr` varchar(255) NOT NULL,
  `newstag` varchar(255) NOT NULL,
  `state` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spider`
--

LOCK TABLES `spider` WRITE;
/*!40000 ALTER TABLE `spider` DISABLE KEYS */;
INSERT INTO `spider` VALUES (1,'jrzj','http://www.jrzj.com','main2_left_fir_left','^(http://www.jrzj.com/)[0-9]{6}(.html)$','news_content',0),(2,'jpm','http://www.jpm.cn','hotspot fl','^(http://www.jpm.cn/article-)[0-9]{5}(-1.html)$','story_box',0),(3,'tencent','http://finance.qq.com','list yaowen','^(http://finance.qq.com/a/)[0-9]{8}\\/[0-9]{6}(.htm)$','qq_article',0),(4,'sohu','http://business.sohu.com','news-list clear','^(http://mt.sohu.com/business/d)[0-9]{8}\\/[0-9]{9}_[0-9]{6}(.shtml)$','text',1),(5,'fenhuang','http://finance.ifeng.com','box_01','^(http://finance.ifeng.com/a/)[0-9]{8}\\/[0-9]{8}(_0.shtml)$','js_selection_area',0),(6,'people','http://finance.people.com.cn','news_box','^(http://finance.people.com.cn/n1/2017)\\/[0-9]{4}\\/c[0-9]{4}-[0-9]{8}(.html)$','box_con',0);
/*!40000 ALTER TABLE `spider` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-04-01 10:35:34
