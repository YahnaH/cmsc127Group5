DROP DATABASE IF EXISTS `tasksApp`;
CREATE DATABASE IF NOT EXISTS `tasksApp`;
USE `tasksApp`;

CREATE TABLE IF NOT EXISTS `user` (
    `userid` VARCHAR(20) NOT NULL,
    `fname` VARCHAR(30) NOT NULL,
    `minit` VARCHAR(30) NOT NULL,
    `lname` VARCHAR(30) NOT NULL,
    `email` VARCHAR(30) NOT NULL,
    `userpassword` VARCHAR(50) NOT NULL,
    CONSTRAINT `user_userid_pk` PRIMARY KEY (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `user` (`userid`, `fname`, `minit`, `lname`, `email`, `userpassword`) VALUES
    ('mjlucero', 'Matthew Jason', 'A', 'Lucero', 'malucero@up.edu.ph', 'abcdefyoumarcoslol');
INSERT INTO `user` (`userid`, `fname`, `minit`, `lname`, `email`, `userpassword`) VALUES
    ('ydahilario', 'Yanna Denise', 'A', 'Hilario', 'malucero@up.edu.ph', 'pythonSample');
INSERT INTO `user` (`userid`, `fname`, `minit`, `lname`, `email`, `userpassword`) VALUES
    ('rmadrid', 'Reinalyn', 'A', 'Madrid', 'rmadrid@up.edu.ph', 'mariaDB123');
INSERT INTO `user` (`userid`, `fname`, `minit`, `lname`, `email`, `userpassword`) VALUES
    ('sample', 'This', 'I', 'ATest', 'testcase@up.edu.ph', 'pass567');

CREATE TABLE IF NOT EXISTS `category` (
    `userid` VARCHAR(20) NOT NULL,
    `categoryid` INT(5) AUTO_INCREMENT,
    `categoryname` VARCHAR(30) NOT NULL,
    `unfinishedtasks` INT(5) DEFAULT NULL,
    CONSTRAINT `category_categoryid_pk` PRIMARY KEY (`categoryid`),
    CONSTRAINT `category_userid_fk` FOREIGN KEY (`userid`) REFERENCES user (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `category` (`userid`, `categoryname`, `unfinishedtasks`) VALUES
    ('sample', 'Acads', NULL);
INSERT INTO `category` (`userid`, `categoryname`, `unfinishedtasks`) VALUES
    ('ydahilario', 'Household Chores', 2);
INSERT INTO `category` (`userid`, `categoryname`, `unfinishedtasks`) VALUES
    ('mjlucero', 'Movie Watchlist', 3);
INSERT INTO `category` (`userid`, `categoryname`, `unfinishedtasks`) VALUES
    ('rmadrid', 'To Buy', NULL);

CREATE TABLE IF NOT EXISTS `task` (
    `userid` VARCHAR(20) NOT NULL,
    `categoryid` INT(5) DEFAULT NULL,
    `taskid` INT(10) NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(30) NOT NULL,
    `details` VARCHAR(70) DEFAULT NULL,
    `deadlinetime` TIME DEFAULT NULL,
    `deadlinedate` DATE DEFAULT NULL,
    `isdone` BOOL DEFAULT 0,
    CONSTRAINT `task_taskid_pk` PRIMARY KEY (`taskid`),
    CONSTRAINT `task_userid_fk` FOREIGN KEY (`userid`) REFERENCES user (`userid`),
    CONSTRAINT `task_categoryid_fk` FOREIGN KEY (`categoryid`) REFERENCES category (`categoryid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `task` (`userid`, `categoryid`, `title`, `details`, `deadlinetime`, `deadlinedate`) VALUES
    ('sample', 1, 'Project Milestone 03', 'SQL Queries', '23:59:59', '2022-05-11');
INSERT INTO `task` (`userid`, `categoryid`, `title`, `details`) VALUES
    ('rmadrid', 4, 'Juice', '5 packs');
INSERT INTO `task` (`userid`, `categoryid`, `title`, `deadlinedate`, `isdone`) VALUES
    ('ydahilario', 2, 'Wash dishes', '2022-05-01', 1);
INSERT INTO `task` (`userid`, `categoryid`, `title`) VALUES
    ('mjlucero', 4, 'Doctor Strange');
INSERT INTO `task` (`userid`, `title`, `details`, `deadlinedate`, `isdone`) VALUES
    ('sample', 'Mop the floor', 'in the bedroom and living room', '2022-05-20', 1);