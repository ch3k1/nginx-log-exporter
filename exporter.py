import argparse
import json
import os
import re
import time

from prometheus_client import start_http_server
from prometheus_client.core import (REGISTRY, CounterMetricFamily,
                                    GaugeMetricFamily)

lineformat = re.compile(
    r"""(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<dateandtime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] ((\"(GET|POST) )(?P<url>.+)(http\/1\.1")) (?P<statuscode>\d{3}) (?P<bytessent>\d+) (["](?P<refferer>(\-)|(.+))["]) (["](?P<useragent>.+)["])""", re.IGNORECASE)
log_path = '/var/log/nginx/access.log'
methods = [
    'get_nginx_total_requests',
    'get_nginx_total_requests_200',
    'get_nginx_total_requests_2xx',
    'get_nginx_total_requests_404',
    'get_nginx_total_requests_4xx',
    'get_nginx_total_requests_500',
    'get_nginx_total_requests_5xx'
]


class NginxCollector(object):
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Nginx custom exporter for prometheus')
        parser.add_argument('-l', dest='logfile',
                            help='Path to nginx log file')
        parser.add_argument('-m', dest='method', required=True)
        args = parser.parse_args()

        if args.method not in methods:
            print("Please use correct method name to start exporter")
            raise SystemExit
        self.method = args.method

        if args.logfile is None:
            self.log_path = log_path
        else:
            self.log_path = args.logfile
        if os.path.exists(self.log_path) is False:
            print("Please setting Up the Access Log")
            raise SystemExit

    def get_nginx_total_requests(self):
        nginx_total_requests = 0
        with open(self.log_path, 'rt') as f:
            for line in f:
                data = re.search(lineformat, line)
                if data is not None:
                    datadict = data.groupdict()
                    if "ipaddress" in datadict:
                        nginx_total_requests += 1
        r = GaugeMetricFamily("nginx_total_requests",
                              'Get nginx total requests', labels=['instance'])
        r.add_metric(["nginx_total_requests"], nginx_total_requests)
        return r

    def get_nginx_total_requests_200(self, code='200'):
        nginx_total_requests_200 = 0
        with open(self.log_path, 'rt') as f:
            for line in f:
                data = re.search(lineformat, line)
                if data is not None:
                    datadict = data.groupdict()
                    if datadict.get('statuscode') == code:
                        nginx_total_requests_200 += 1
        r = GaugeMetricFamily("nginx_total_requests_200",
                              'Get nginx total requests by status code(200)', labels=['instance'])
        r.add_metric(["nginx_total_requests_200"], nginx_total_requests_200)
        return r

    def get_nginx_total_requests_2xx(self, code_start='200', code_end='226'):
        nginx_total_requests_2xx = 0
        with open(self.log_path, 'rt') as f:
            for line in f:
                data = re.search(lineformat, line)
                if data is not None:
                    datadict = data.groupdict()
                    is_between = int(datadict.get('statuscode')) in range(
                        int(code_start), int(code_end))
                    if is_between is True:
                        nginx_total_requests_2xx += 1
        r = GaugeMetricFamily("nginx_total_requests_2xx",
                              'Get nginx total requests by status code(2xx)', labels=['instance'])
        r.add_metric(["nginx_total_requests_2xx"], nginx_total_requests_2xx)
        return r

    def get_nginx_total_requests_404(self, code='404'):
        nginx_total_requests_404 = 0
        with open(self.log_path, 'rt') as f:
            for line in f:
                data = re.search(lineformat, line)
                if data is not None:
                    datadict = data.groupdict()
                    if datadict.get('statuscode') == code:
                        nginx_total_requests_404 += 1
        r = GaugeMetricFamily("nginx_total_requests_404",
                              'Get nginx total requests by status code(404)', labels=['instance'])
        r.add_metric(["nginx_total_requests_404"], nginx_total_requests_404)
        return r

    def get_nginx_total_requests_4xx(self, code_start='400', code_end='451'):
        nginx_total_requests_4xx = 0
        with open(self.log_path, 'rt') as f:
            for line in f:
                data = re.search(lineformat, line)
                if data is not None:
                    datadict = data.groupdict()
                    is_between = int(datadict.get('statuscode')) in range(
                        int(code_start), int(code_end))
                    if is_between is True:
                        nginx_total_requests_4xx += 1
        r = GaugeMetricFamily("nginx_total_requests_4xx",
                              'Get nginx total requests by status code(4xx)', labels=['instance'])
        r.add_metric(["nginx_total_requests_4xx"], nginx_total_requests_4xx)
        return r

    def get_nginx_total_requests_500(self, code='500'):
        nginx_total_requests_500 = 0
        with open(self.log_path, 'rt') as f:
            for line in f:
                data = re.search(lineformat, line)
                if data is not None:
                    datadict = data.groupdict()
                    if datadict.get('statuscode') == code:
                        nginx_total_requests_500 += 1
        r = GaugeMetricFamily("nginx_total_requests_500",
                              'Get nginx total requests by status code(500)', labels=['instance'])
        r.add_metric(["nginx_total_requests_500"], nginx_total_requests_500)
        return r

    def get_nginx_total_requests_5xx(self, code_start='500', code_end='511'):
        nginx_total_requests_5xx = 0
        with open(self.log_path, 'rt') as f:
            for line in f:
                data = re.search(lineformat, line)
                if data is not None:
                    datadict = data.groupdict()
                    is_between = int(datadict.get('statuscode')) in range(
                        int(code_start), int(code_end))
                    if is_between is True:
                        nginx_total_requests_5xx += 1
        r = GaugeMetricFamily("nginx_total_requests_5xx",
                              'Get nginx total requests by status code(5xx)', labels=['instance'])
        r.add_metric(["nginx_total_requests_5xx"], nginx_total_requests_5xx)
        return r

    def collect(self):
        method = getattr(self, self.method)
        yield method()


if __name__ == '__main__':
    try:
        start_http_server(8000)
        REGISTRY.register(NginxCollector())
        while True:
            time.sleep(1)
    except:
        print("Nginx exporter stoped")
        raise SystemExit
