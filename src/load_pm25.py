#!/usr/bin/env python
#coding=utf-8

import sys
import os.path
from datetime import datetime
import time
import requests
from optparse import OptionParser

# parse option
option_parser = OptionParser()
option_parser.add_option('--output_dir', default='/mydata/pm25', metavar='output directory')
option_parser.add_option('--token', metavar='pm25.in appkey')

options, args = option_parser.parse_args(sys.argv[1:])

# 测试用的token, 经常过期
token = {'token': '5j1znBVAsnSf5xQyNQyq'}
cookies = {}

# 使用测试token的cookies模拟
token = {}
cookies = {
    '_aqi_query_session': 'BAh7CUkiD3Nlc3Npb25faWQGOgZFRkkiJTE2OTBlYmVmZTI0ZGQxNWUyMmU4NDg0MTVkMjUwNmMyBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMVVQeFdvVStiRi9sT3JhYUl3SUZ1OGpRSjk3RVBvSFpSODRXRzZFYlRYczg9BjsARkkiDGNhcHRjaGEGOwBGIi00ODE2ZTEyMmQ2YmM2NDVhN2QzMzdiZTZhYWFlOTY4MzRiYmVkNmMzSSIdd2FyZGVuLnVzZXIuYXBpX3VzZXIua2V5BjsAVFsHWwZpAkIDSSIiJDJhJDEwJFhGQzRsazhwOFdOOFZUWHVQaXl3R08GOwBU--1c25a8d8a1a062e5cdec873f8e6e0caab6c7d249',
    '__utma': '162682429.1633318175.1447736776.1447736776.1447740792.2',
    '__utmb': '162682429.6.10.1447830189',
    '__utmc': '162682429',
    '__utmt': '1',
    '__utmz': '162682429.1447736776.1.1.utmcsr=bing|utmccn=(organic)|utmcmd=organic|utmctr=pm25'}

if options.token is not None:
    token = options.token
    cookies = {}

output_dir = options.output_dir
if not os.path.isdir(output_dir):
    os.makedirs(output_dir)


def get_stations():
    url = "http://www.pm25.in/api/querys/station_names.json"
    try:
        stat_file = open(os.path.join(output_dir, 'stations.csv'), 'w')
        req = requests.get(url, params = token, cookies = cookies, timeout = (5, 90))
        stations = req.json()
        if 'error' in stations:
            print req.text
            return False
        for it in stations:
            city = it['city']
            stats = it['stations']
            for it2 in stats:
                stat_name = it2['station_name']
                stat_code = it2['station_code']
                stat_file.write('%s,%s,%s\n' % (city.encode('utf-8'), stat_name.encode('utf-8'), stat_code.encode('utf-8')))
        stat_file.close()
        return True
    except Exception,ex:
        print datetime.now()
        print Exception,":",ex
        return False

def check_none_value(dd):
    for it in dd:
        if dd[it] is None:
            dd[it] = 'null'


def get_now_data():
    url = "http://www.pm25.in/api/querys/all_cities.json"
    timestamp = None
    update_data = False
    try:
        timestamp_f = open(os.path.join(output_dir, 'timestamp'), 'r')
        str_timestamp = timestamp_f.readline()
        timestamp = datetime.strptime(str_timestamp, "%Y-%m-%dT%H:%M:%SZ")
        timestamp_f.close()
    except:
        pass

    try:
        req = requests.get(url, params = token, cookies = cookies, timeout = (5, 90))
        result = req.json()
        if 'error' in result:
            print str(datetime.now())
            print req.text
            return False
        for it in result:
            if 'station_code' not in it or it['station_code'] is None:
                print 'get station_code error'
                continue
            stat_code = it['station_code'].encode('utf-8')
            if not update_data:
                cur_time = datetime.strptime(it['time_point'].encode('utf-8'), "%Y-%m-%dT%H:%M:%SZ")
                if timestamp and timestamp == cur_time:
                    print str(datetime.now()), 'waiting for next hour to update data\n'
                    return True
                else:
                    update_data = True
                    timestamp_f = open(os.path.join(output_dir, 'timestamp'), 'w')
                    timestamp_f.write(cur_time.strftime("%Y-%m-%dT%H:%M:%SZ"))
                    timestamp_f.close()
            if update_data is True:
                fp = open(os.path.join(output_dir, stat_code + '.csv'), 'a+')
                check_none_value(it)
                fp.write('%s,%s,%s' % (it['area'].encode('utf-8'), it['position_name'].encode('utf-8'), it['station_code'].encode('utf-8')))
                fp.write(',%s,%s,%s' % (it['time_point'].encode('utf-8'), it['quality'].encode('utf-8'), it['primary_pollutant'].encode('utf-8')))
                fp.write(',%d' % it['aqi'])
                fp.write(',%d,%d' % (it['pm2_5'], it['pm2_5_24h']))
                fp.write(',%d,%d' % (it['pm10'], it['pm10_24h']))
                fp.write(',%d,%d' % (it['co'], it['co_24h']))
                fp.write(',%d,%d' % (it['no2'], it['no2_24h']))
                fp.write(',%d,%d' % (it['o3'], it['o3_24h']))
                fp.write(',%d,%d' % (it['o3_8h'], it['o3_8h_24h']))
                fp.write(',%d,%d\n' % (it['so2'], it['so2_24h']))
                fp.close()
        print str(datetime.now()), 'updated data\n'
        return True
    except Exception,ex:
        print datetime.now()
        print ex
        return False

def main():
    success = get_stations()
    if success:
        while(True):
            success = False
            failed_count = 0
            while(not success):
                success = get_now_data()
                if not success:
                    failed_count += 1
                    time.sleep(60)
            time.sleep(3600)
    else:
        print "init failed, pm25.in refused"


if __name__ == '__main__':
    main()
