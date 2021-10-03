-- 2021-09-05
-- Alter tables

alter table `ACCOUNT` add `timezone` varchar(100);

alter table `SESSION` add `completed` tinyint default 0;
alter table `SESSION` add `deleted` tinyint default 0;
