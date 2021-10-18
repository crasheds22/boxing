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

RUN apt-get install -y default-libmysqlclient-dev

RUN a2enmod cgid

RUN a2dissite 000-default

RUN ln -sf /var/www/html ./html
RUN mkdir /var/www/cgi-bin
RUN ln -sf /var/www/cgi-bin ./cgi-bin

RUN ln -sf /dev/stderr /var/log/apache2/error.log
RUN ln -sf /dev/stdout /var/log/apache2/access.log

RUN cpan -y DBI Data::UUID Template JSON Try::Tiny DBD::mysql CGI Digest::SHA;

RUN echo '\n\
    <VirtualHost *:80>\n\
        DocumentRoot "/var/www/html"\n\
        DirectoryIndex /cgi-bin/login.cgi\n\
        ErrorLog /dev/stderr\n\
        CustomLog /dev/stdout common\n\
    </VirtualHost>' >> /etc/apache2/sites-available/boxing.conf

RUN a2ensite boxing

EXPOSE 80

CMD ["/usr/sbin/apachectl", "-DFOREGROUND"]
