create table if not exists `ACTIVITY_TYPE` (
	`typeid` int not null auto_increment,
    `typename` varchar(45),
    primary key (`typeid`)
) Engine=InnoDB;

create table if not exists `STAFF_TYPE` (
	`typeid` int not null auto_increment,
    `typename` varchar(45),
    primary key (`typeid`)
) Engine=InnoDB;

create table if not exists `ACTIVITY` (
	`activityid` int not null auto_increment,
    `activityname` varchar(45),
    `instructions` json,
    `deleted` tinyint default 0,
    `typeid` int not null,
    primary key (`activityid`),
    foreign key (`typeid`) references `ACTIVITY_TYPE` (`typeid`)
) Engine=InnoDB;

create table if not exists `ACCOUNT` (
	`accountid` int not null auto_increment,
    `accountname` varchar(100),
    `username` varchar(100),
    `password` varchar(256),
    `insertdate` date,
    `archived` tinyint default 0,
    `deleted` tinyint default 0,
    primary key (`accountid`)
) Engine=InnoDB;

create table if not exists `CLINICIAN` (
	`stafftypeid` int not null,
    `clinicianid` int not null,
    foreign key (`stafftypeid`) references `STAFF_TYPE` (`typeid`),
    foreign key (`clinicianid`) references `ACCOUNT` (`accountid`)
) Engine=InnoDB;

create table if not exists `PATIENT` (
	`patientid` int not null,
    `dob` date,
    `condition` varchar(100),
    `height` int,
    `weight` int,
    `armlength` int,
    foreign key (`patientid`) references `ACCOUNT` (`accountid`)
) Engine=InnoDB;

create table if not exists `APPOINTMENT` (
	`appointmentid` int not null auto_increment,
    `clinicianid` int not null,
    `patientid` int not null,
    `bookingtime` datetime,
    primary key (`appointmentid`),
    foreign key (`clinicianid`) references `CLINICIAN` (`clinicianid`),
    foreign key (`patientid`) references `PATIENT` (`patientid`)
) Engine=InnoDB;

create table if not exists `ACTIVITY_ACCESS` (
	`activityid` int not null,
    `clinicianid` int not null,
    foreign key (`activityid`) references `ACTIVITY` (`activityid`),
    foreign key (`clinicianid`) references `CLINICIAN` (`clinicianid`)
) Engine=InnoDB;

create table if not exists `SESSION` (
	`sessionid` int not null auto_increment,
    `sessionname` varchar(45),
    `scheduledfor` datetime,
    primary key (`sessionid`)
) Engine=InnoDB;

create table if not exists `EXERCISE` (
	`exerciseid` int not null auto_increment,
    `exercisename` varchar(45),
    `sessionorder` int,
    `exercisedata` json,
    `completedon` datetime,
    `insertdate` date,
    `sessionid` int not null,
    `activityid` int not null,
    `patientid` int not null,
    `clinicianid` int not null,
    primary key (`exerciseid`),
    foreign key (`sessionid`) references `SESSION` (`sessionid`),
    foreign key (`activityid`) references `ACTIVITY` (`activityid`),
    foreign key (`patientid`) references `PATIENT` (`patientid`),
    foreign key (`clinicianid`) references `CLINICIAN` (`clinicianid`)
) Engine=InnoDB;
