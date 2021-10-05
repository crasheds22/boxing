CREATE DATABASE  IF NOT EXISTS `boxing` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `boxing`;
-- MySQL dump 10.13  Distrib 8.0.26, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: boxing
-- ------------------------------------------------------
-- Server version	8.0.26

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
-- Table structure for table `ACCOUNT`
--

DROP TABLE IF EXISTS `ACCOUNT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ACCOUNT` (
  `accountid` int NOT NULL AUTO_INCREMENT,
  `accountname` varchar(100) DEFAULT NULL,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(256) DEFAULT NULL,
  `insertdate` date DEFAULT NULL,
  `archived` tinyint DEFAULT '0',
  `deleted` tinyint DEFAULT '0',
  `timezone` varchar(100) DEFAULT NULL,
  `accounttypeid` int DEFAULT NULL,
  PRIMARY KEY (`accountid`),
  KEY `accounttypeid` (`accounttypeid`),
  CONSTRAINT `account_ibfk_1` FOREIGN KEY (`accounttypeid`) REFERENCES `ACCOUNT_TYPE` (`typeid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ACCOUNT_TYPE`
--

DROP TABLE IF EXISTS `ACCOUNT_TYPE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ACCOUNT_TYPE` (
  `typeid` int NOT NULL AUTO_INCREMENT,
  `typename` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`typeid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ACTIVITY`
--

DROP TABLE IF EXISTS `ACTIVITY`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ACTIVITY` (
  `activityid` int NOT NULL AUTO_INCREMENT,
  `activityname` varchar(45) DEFAULT NULL,
  `instructions` json DEFAULT NULL,
  `deleted` tinyint DEFAULT '0',
  `typeid` int NOT NULL,
  `insertdate` date DEFAULT NULL,
  `modifieddate` date DEFAULT NULL,
  PRIMARY KEY (`activityid`),
  KEY `typeid` (`typeid`),
  CONSTRAINT `activity_ibfk_1` FOREIGN KEY (`typeid`) REFERENCES `ACTIVITY_TYPE` (`typeid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ACTIVITY_ACCESS`
--

DROP TABLE IF EXISTS `ACTIVITY_ACCESS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ACTIVITY_ACCESS` (
  `activityid` int NOT NULL,
  `clinicianid` int NOT NULL,
  KEY `activityid` (`activityid`),
  KEY `clinicianid` (`clinicianid`),
  CONSTRAINT `activity_access_ibfk_1` FOREIGN KEY (`activityid`) REFERENCES `ACTIVITY` (`activityid`),
  CONSTRAINT `activity_access_ibfk_2` FOREIGN KEY (`clinicianid`) REFERENCES `CLINICIAN` (`clinicianid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ACTIVITY_HISTORY`
--

DROP TABLE IF EXISTS `ACTIVITY_HISTORY`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ACTIVITY_HISTORY` (
  `historyid` int NOT NULL AUTO_INCREMENT,
  `activityid` int NOT NULL,
  `insertdate` datetime DEFAULT NULL,
  PRIMARY KEY (`historyid`),
  KEY `activityid` (`activityid`),
  CONSTRAINT `activity_history_ibfk_1` FOREIGN KEY (`activityid`) REFERENCES `ACTIVITY` (`activityid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ACTIVITY_TYPE`
--

DROP TABLE IF EXISTS `ACTIVITY_TYPE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ACTIVITY_TYPE` (
  `typeid` int NOT NULL AUTO_INCREMENT,
  `typename` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`typeid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `APPOINTMENT`
--

DROP TABLE IF EXISTS `APPOINTMENT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `APPOINTMENT` (
  `appointmentid` int NOT NULL AUTO_INCREMENT,
  `clinicianid` int NOT NULL,
  `patientid` int NOT NULL,
  `bookingtime` datetime DEFAULT NULL,
  PRIMARY KEY (`appointmentid`),
  KEY `clinicianid` (`clinicianid`),
  KEY `patientid` (`patientid`),
  CONSTRAINT `appointment_ibfk_1` FOREIGN KEY (`clinicianid`) REFERENCES `CLINICIAN` (`clinicianid`),
  CONSTRAINT `appointment_ibfk_2` FOREIGN KEY (`patientid`) REFERENCES `PATIENT` (`patientid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `CLINICIAN`
--

DROP TABLE IF EXISTS `CLINICIAN`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CLINICIAN` (
  `clinicianid` int NOT NULL,
  KEY `clinicianid` (`clinicianid`),
  CONSTRAINT `clinician_ibfk_2` FOREIGN KEY (`clinicianid`) REFERENCES `ACCOUNT` (`accountid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `EXERCISE`
--

DROP TABLE IF EXISTS `EXERCISE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `EXERCISE` (
  `exerciseid` int NOT NULL AUTO_INCREMENT,
  `exercisename` varchar(45) DEFAULT NULL,
  `sessionorder` int DEFAULT NULL,
  `exercisedata` json DEFAULT NULL,
  `completedon` datetime DEFAULT NULL,
  `insertdate` date DEFAULT NULL,
  `sessionid` int NOT NULL,
  `activityid` int NOT NULL,
  PRIMARY KEY (`exerciseid`),
  KEY `sessionid` (`sessionid`),
  KEY `activityid` (`activityid`),
  CONSTRAINT `exercise_ibfk_1` FOREIGN KEY (`sessionid`) REFERENCES `SESSION` (`sessionid`),
  CONSTRAINT `exercise_ibfk_2` FOREIGN KEY (`activityid`) REFERENCES `ACTIVITY` (`activityid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `PATIENT`
--

DROP TABLE IF EXISTS `PATIENT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PATIENT` (
  `patientid` int NOT NULL,
  `dob` date DEFAULT NULL,
  `condition` varchar(100) DEFAULT NULL,
  `height` int DEFAULT NULL,
  `weight` int DEFAULT NULL,
  `armlength` int DEFAULT NULL,
  `insertby` int NOT NULL,
  KEY `patientid` (`patientid`),
  KEY `insertby` (`insertby`),
  CONSTRAINT `patient_ibfk_1` FOREIGN KEY (`patientid`) REFERENCES `ACCOUNT` (`accountid`),
  CONSTRAINT `patient_ibfk_2` FOREIGN KEY (`insertby`) REFERENCES `CLINICIAN` (`clinicianid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `REPORTING`
--

DROP TABLE IF EXISTS `REPORTING`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `REPORTING` (
  `headclinician` int NOT NULL,
  `clinicianid` int NOT NULL,
  KEY `headclinician` (`headclinician`),
  KEY `clinicianid` (`clinicianid`),
  CONSTRAINT `reporting_ibfk_1` FOREIGN KEY (`headclinician`) REFERENCES `CLINICIAN` (`clinicianid`),
  CONSTRAINT `reporting_ibfk_2` FOREIGN KEY (`clinicianid`) REFERENCES `CLINICIAN` (`clinicianid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `SESSION`
--

DROP TABLE IF EXISTS `SESSION`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SESSION` (
  `sessionid` int NOT NULL AUTO_INCREMENT,
  `sessionname` varchar(45) DEFAULT NULL,
  `scheduledfor` datetime DEFAULT NULL,
  `completed` tinyint DEFAULT '0',
  `deleted` tinyint DEFAULT '0',
  `patientid` int NOT NULL,
  `clinicianid` int NOT NULL,
  PRIMARY KEY (`sessionid`),
  KEY `patientid` (`patientid`),
  KEY `clinicianid` (`clinicianid`),
  CONSTRAINT `session_ibfk_1` FOREIGN KEY (`patientid`) REFERENCES `PATIENT` (`patientid`),
  CONSTRAINT `session_ibfk_2` FOREIGN KEY (`clinicianid`) REFERENCES `CLINICIAN` (`clinicianid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-10-05 18:24:28
