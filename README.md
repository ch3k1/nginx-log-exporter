Reads an Nginx log file to get total requests by status code and exports metrics to Prometheus.

## Installation ##

## Docker ##

```
docker build . -t nginx-exporter
```

```
docker run -p 8080:80 -p 8000:8000 --name nginx-exporter -d nginx-exporter
```

### Usage

#### Run the exporter

```
docker exec -d nginx-exporter python3 exporter.py -m get_nginx_total_requests
``` 

## Manual installation ##

```
pip install -r requirements.txt
```

### Usage

#### Run the exporter

```
python3 exporter.py -m get_nginx_total_requests
```

## Methods

```
get_nginx_total_requests
get_nginx_total_requests_200
get_nginx_total_requests_2xx
get_nginx_total_requests_404
get_nginx_total_requests_4xx
get_nginx_total_requests_500
get_nginx_total_requests_5xx
```

## Supported Python Versions

```
2.7.x and greater
```