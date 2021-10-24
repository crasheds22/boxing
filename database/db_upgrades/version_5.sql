-- 2021-10-24
-- AT

alter table `SESSION`
modify column `scheduledfor` date;

alter table `SESSION`
modify column `completed` date null;
