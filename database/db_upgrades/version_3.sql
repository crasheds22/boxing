-- 2021-10-21
-- AT: Various

insert into `ACTIVITY_TYPE` ( `typename` )
values ( 'Static Targets' );

drop table `ACTIVITY_HISTROY`;

alter table `ACTIVITY`
add column `prev_version` int,
add constraint activity_ibfk_2 foreign key (`prev_version`) references `ACTIVITY`(`activityid`);

insert into `ACCOUNT` (accountid, accountname)
values (-1, 'Everybody');
