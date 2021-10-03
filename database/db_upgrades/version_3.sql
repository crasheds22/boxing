-- 07/09/2021
-- Add REPORTING and ACTIVITY_HISTORY

create table if not exists `ACTIVITY_HISTORY` (
    `historyid` int not null auto_increment,
    `activityid` int not null,
    `insertdate` datetime,
    primary key (`historyid`),
    foreign key (`activityid`) references `ACTIVITY` (`activityid`)
) Engine=InnoDB;

create table if not exists `REPORTING` (
    `headclinician` int not null,
    `clinicianid` int not null,
    foreign key (`headclinician`) references `CLINICIAN` (`clinicianid`),
    foreign key (`clinicianid`) references `CLINICIAN` (`clinicianid`)
) Engine=InnoDB;

alter table `ACTIVITY` add `insertdate` date;
alter table `ACTIVITY` add `modifieddate` date;
