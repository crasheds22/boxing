-- 2021-10-17
-- AT ACCOUNT_SESSION and ACCOUNT_LOG tables

create table `ACCOUNT_SESSION` (
    `id` int auto_increment,
    `sessionid` varchar(128),
    `accountid` int,
    `insertdate` datetime,
    `last_seen` datetime,
    primary key (`id`),
    foreign key (`accountid`) references `ACCOUNT` (`accountid`)
) Engine=`InnoDB`;

create table `ACCOUNT_LOG` (
    `logid` int auto_increment,
    `accountid` int,
    `sessionid` varchar(128),
    `insertdate` datetime,
    primary key (`logid`),
    foreign key (`accountid`) references `ACCOUNT` (`accountid`) 
) Engine=`InnoDB`;