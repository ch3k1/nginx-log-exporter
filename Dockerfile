FROM ubuntu:focal

RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

RUN apt-get update && apt-get -y install curl gnupg2 ca-certificates lsb-release git \
    net-tools python3-distutils python3-apt \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py

RUN echo "deb http://nginx.org/packages/ubuntu `lsb_release -cs` nginx" \
    | tee /etc/apt/sources.list.d/nginx.list

RUN curl -o /tmp/nginx_signing.key https://nginx.org/keys/nginx_signing.key \ 
    && mv /tmp/nginx_signing.key /etc/apt/trusted.gpg.d/nginx_signing.asc \
    && apt-get update && apt-get -y install nginx

WORKDIR /nginx-exporter
ENV LANG en_US.utf8

COPY . .
RUN pip install -r requirements.txt
COPY nginx/nginx.conf /etc/nginx/nginx.conf
EXPOSE 80 8000

STOPSIGNAL SIGTERM
CMD ["nginx", "-g", "daemon off;"]