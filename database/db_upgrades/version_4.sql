-- 08/09/2021
-- More changes

alter table `PATIENT` 
    add `insertby` int not null,
    add foreign key (`insertby`) references `CLINICIAN` (`clinicianid`);

alter table `CLINICIAN` 
    drop constraint `clinician_ibfk_1`,
    drop column `stafftypeid`;

drop table `STAFF_TYPE`;

create table `ACCOUNT_TYPE` (
    `typeid` int not null auto_increment,
    `typename` varchar(100),
    primary key (`typeid`)
) Engine=InnoDB;

alter table `ACCOUNT` 
    add `accounttypeid` int,
    add foreign key (`accounttypeid`) references `ACCOUNT_TYPE` (`typeid`);

alter table `EXERCISE`
    drop constraint `exercise_ibfk_3`,
    drop constraint `exercise_ibfk_4`,
    drop column `patientid`,
    drop column `clinicianid`;

alter table `SESSION`
    add `patientid` int not null,
    add `clinicianid` int not null,
    add foreign key (`patientid`) references `PATIENT` (`patientid`),
    add foreign key (`clinicianid`) references `CLINICIAN` (`clinicianid`);


