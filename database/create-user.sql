create user 'slaveuser'@'%' identified by 'slavepass';
grant all privileges on *.* to 'slaveuser'@'%';
flush privileges;