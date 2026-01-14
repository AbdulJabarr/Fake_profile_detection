-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 28, 2024 at 06:05 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `python_fake_profile_detection`
--

-- --------------------------------------------------------

--
-- Table structure for table `chat_details`
--

CREATE TABLE `chat_details` (
  `id` int(100) NOT NULL,
  `sender` varchar(100) NOT NULL,
  `receiver` varchar(100) NOT NULL,
  `message` varchar(100) NOT NULL,
  `date` varchar(100) NOT NULL,
  `time` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `report` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `chat_details`
--


-- --------------------------------------------------------

--
-- Table structure for table `comments_details`
--

CREATE TABLE `comments_details` (
  `id` int(100) NOT NULL,
  `pid` varchar(100) NOT NULL,
  `sender` varchar(100) NOT NULL,
  `comments` varchar(100) NOT NULL,
  `date` varchar(100) NOT NULL,
  `time` varchar(100) NOT NULL,
  `match_result` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `report` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `comments_details`
--


-- --------------------------------------------------------

--
-- Table structure for table `friends_details`
--

CREATE TABLE `friends_details` (
  `id` int(100) NOT NULL,
  `user` varchar(100) NOT NULL,
  `receiver` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `friends_details`
--


-- --------------------------------------------------------

--
-- Table structure for table `tweet_details`
--

CREATE TABLE `tweet_details` (
  `id` int(100) NOT NULL,
  `user` varchar(100) NOT NULL,
  `subject` varchar(100) NOT NULL,
  `cdate` varchar(100) NOT NULL,
  `ctime` varchar(100) NOT NULL,
  `filename` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `report` varchar(100) NOT NULL,
  `matching` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tweet_details`
--


-- --------------------------------------------------------

--
-- Table structure for table `user_details`
--

CREATE TABLE `user_details` (
  `id` int(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `contact` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `address` varchar(100) NOT NULL,
  `gender` varchar(100) NOT NULL,
  `dob` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `report` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user_details`
--

