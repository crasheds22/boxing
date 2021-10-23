-- 2021-10-23
-- AT: changes

alter table `EXERCISE`
drop column `exercisename`, 
drop column `completedon`, 
drop column `insertdate`;

insert into ACTIVITY_TYPE (typename)
values ("Dynamic Training"), ("Rest Period") ;
