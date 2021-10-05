FROM mysql:latest

ENV MYSQL_USER=user
ENV MYSQL_PASSWORD=password
ENV MYSQL_DATABASE=boxing
ENV MYSQL_ROOT_PASSWORD=password

COPY boxing-schema.sql /docker-entrypoint-initdb.d/
COPY create-user.sql /docker-entrypoint-initdb.d/

COPY connect-db.sh /usr/bin/

EXPOSE 3306

CMD ["mysqld"]