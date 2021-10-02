FROM ubuntu:16.04

RUN apt-get update && apt-get upgrade

RUN apt-get install -y build-essential

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Australia/Perth
RUN apt-get install -y tzdata

RUN apt-get install -y \
    apache2 \
    curl \
    perl

RUN a2enmod cgid

EXPOSE 80

CMD ["/usr/sbin/apachectl", "-DFOREGROUND"]
