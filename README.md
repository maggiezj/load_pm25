# Load PM2.5 Data

使用 www.pm25.in 提供的API接口下载PM2.5相关数据

## 安装

	python setup.py install


## 运行

	load_pm25.py --output_dir=./output --token=5j1znBVAsnSf5xQyNQyq

注: 请使用 pm25.in 正式授权的appkey替换掉示例中的测试appkey

## 输出文件

* station.csv

	city,station_name,station_code

* station_code.csv

	city,station_name,station_code,time_point,quality,primary_pollutant,aqi,pm2_5,pm2_5_24h,pm10,pm10_24h,co,co_24h,no2,no2_24h,o3,o3_24h,o3_8h,o3_8h_24h,so2,so2_24h

注: coding=utf-8
