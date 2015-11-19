# Load PM2.5 Data Using www.pm25.in API

## 安装

python setup.py install


## 运行

load_pm25.py --output_dir=./output --token=5j1znBVAsnSf5xQyNQyq
注：请使用 www.pm25.in 正式授权的apikey替换掉示例中的测试apikey

## 输出文件结构

* station.csv 结构

	#city #station_name #station_code

* station_code.csv 结构

	#city #station_name #station_code #time_point #quality #primary_pollutant #aqi #pm2_5 #pm2_5_24h #pm10 #pm10_24h #co #co_24h #no2 #no2_24h #o3 #o3_24h #o3_8h #o3_8h_24h #so2 #so2_24h