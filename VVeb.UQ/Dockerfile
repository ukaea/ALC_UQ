# --- Dockerfile to run both Apache2-PHP and Docker-in-Docker
FROM alpine:3.10
MAINTAINER stanislas.pamela@ukaea.uk

# --- Install Docker wrapper.
ADD ./wrapdocker /usr/local/bin/wrapdocker

# --- Install Docker and dependencies
RUN apk --update add \
  bash \
  iptables \
  ca-certificates \
  e2fsprogs \
  docker \
  curl \
  zip \
  perl \
  php-apache2 php-cli php-json php-mbstring php-phar php-openssl \
  && chmod +x /usr/local/bin/wrapdocker \
  && rm -rf /var/cache/apk/* \
  && curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
  && mkdir -p /var/www/html/ && chown -R apache:apache /var/www/html

# --- Copy data
COPY www/ /var/www/html/
COPY config.in /var/www/html/php/
COPY etc/apache2/httpd.conf /etc/apache2/httpd.conf
COPY etc/apache2/sites/ /etc/apache2/sites/
COPY etc/php/php.ini /etc/php7/php.ini
COPY entrypoint.sh /opt/entrypoint.sh

# --- Expose port
EXPOSE 80

# --- Run container
VOLUME /var/lib/docker
WORKDIR /var/www/html/
RUN chmod +x /opt/entrypoint.sh
CMD ["wrapdocker"]
ENTRYPOINT [ "/opt/entrypoint.sh" ]

