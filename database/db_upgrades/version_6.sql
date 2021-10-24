-- 2021-10-24
-- AT

alter table `ACCOUNT`
drop column `password`;

update `ACCOUNT` set `insertdate`=UTC_TIMESTAMP();

update `ACCOUNT` set `username`='000001' where `accountid`=1;
update `ACCOUNT` set `username`='000002' where `accountid`=2;
update `ACCOUNT` set `username`='000003' where `accountid`=3;
update `ACCOUNT` set `username`='000004' where `accountid`=4;

alter table `ACCOUNT`
modify column `username` char(6);
