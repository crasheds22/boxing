FROM httpd

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y build-essential

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Australia/Perth
RUN apt-get install -y tzdata

RUN apt-get install -y \
    apache2 \
    curl \
    perl \
    vim \
    nano

RUN a2enmod cgid

RUN ln -sf /dev/stderr /var/log/apache2/error.log
RUN ln -sf /dev/stdout /var/log/apache2/access.log

RUN cpan -y DBI
RUN cpan -y Template

EXPOSE 80

CMD ["/usr/sbin/apachectl", "-DFOREGROUND"]
