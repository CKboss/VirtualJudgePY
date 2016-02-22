-- MySQL dump 10.13  Distrib 5.6.28, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: mydb
-- ------------------------------------------------------
-- Server version	5.6.28-0ubuntu0.14.04.1

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
-- Table structure for table `contest`
--

DROP TABLE IF EXISTS `contest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contest` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `ctitle` varchar(255) DEFAULT NULL,
  `cdescription` text,
  `announcement` text,
  `password` varchar(45) DEFAULT NULL,
  `begintime` datetime DEFAULT NULL,
  `endtime` datetime DEFAULT NULL,
  `hashcode` varchar(255) DEFAULT NULL,
  `ispublic` tinyint(1) DEFAULT NULL,
  `cuid` int(11) DEFAULT NULL,
  `cstatus` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`cid`),
  KEY `fk_contest_1_idx` (`cuid`),
  CONSTRAINT `fk_contest_1` FOREIGN KEY (`cuid`) REFERENCES `user` (`uid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cproblem`
--

DROP TABLE IF EXISTS `cproblem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cproblem` (
  `cpid` int(11) NOT NULL AUTO_INCREMENT,
  `cid` int(11) DEFAULT NULL,
  `pid` int(11) DEFAULT NULL,
  `title` varchar(45) DEFAULT NULL,
  `originOJ` varchar(45) DEFAULT NULL,
  `originProb` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`cpid`),
  KEY `fk_cproblem_1_idx` (`cid`),
  KEY `fk_cproblem_2_idx` (`pid`),
  CONSTRAINT `fk_cproblem_1` FOREIGN KEY (`cid`) REFERENCES `contest` (`cid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_cproblem_2` FOREIGN KEY (`pid`) REFERENCES `problem` (`pid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `problem`
--

DROP TABLE IF EXISTS `problem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `problem` (
  `pid` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `source` text,
  `url` varchar(1024) DEFAULT NULL,
  `originOJ` varchar(45) DEFAULT NULL,
  `originProb` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=8967 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `problemdetail`
--

DROP TABLE IF EXISTS `problemdetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `problemdetail` (
  `did` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) DEFAULT NULL,
  `description` text,
  `input` text,
  `output` text,
  `sampleinput` text,
  `sampleoutput` text,
  `hint` text,
  `author` varchar(255) DEFAULT NULL,
  `source` varchar(255) DEFAULT NULL,
  `updatetime` datetime DEFAULT NULL,
  `memorylimit` varchar(45) DEFAULT NULL,
  `timelimit` varchar(45) DEFAULT NULL,
  `specialjudge` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`did`),
  KEY `fk_problemdetail_1_idx` (`pid`),
  CONSTRAINT `fk_problemdetail_1` FOREIGN KEY (`pid`) REFERENCES `problem` (`pid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=8929 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `status`
--

DROP TABLE IF EXISTS `status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status` (
  `sid` int(11) NOT NULL AUTO_INCREMENT,
  `timesubmit` datetime DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `runtime` varchar(45) DEFAULT NULL,
  `runmemory` varchar(45) DEFAULT NULL,
  `pid` int(11) DEFAULT NULL,
  `cid` int(11) DEFAULT NULL,
  `language` varchar(45) DEFAULT NULL,
  `source` text,
  `isopen` tinyint(1) DEFAULT NULL,
  `uid` int(11) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `originOJ` varchar(255) DEFAULT NULL,
  `originProb` varchar(45) DEFAULT NULL,
  `realrunid` varchar(45) DEFAULT NULL,
  `isdisplay` tinyint(1) DEFAULT NULL,
  `ceinfo` text,
  `codelenth` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`sid`),
  KEY `fk_status_1_idx` (`pid`),
  CONSTRAINT `fk_status_1` FOREIGN KEY (`pid`) REFERENCES `problem` (`pid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `nickname` varchar(1024) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `school` varchar(255) DEFAULT NULL,
  `localstatus` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`uid`,`username`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-02-22 22:51:06