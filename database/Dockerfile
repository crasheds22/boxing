FROM mysql:5.7

ENV MYSQL_DATABASE=boxing
ENV MYSQL_ROOT_PASSWORD=password

COPY boxing-schema.sql /docker-entrypoint-initdb.d/
COPY boxing-data.sql /docker-entrypoint-initdb.d/boxing-zz-data.sql
COPY create-user.sql /docker-entrypoint-initdb.d/

COPY connect-db.sh /usr/bin/

CMD ["mysqld"]