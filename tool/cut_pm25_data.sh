#!/bin/bash

PM25DATA_DIR='/mydata/pm25_data'

LASTMONTH=$(date -d "yesterday" +%Y%m)


mv -f ${PM25DATA_DIR} ${PM25DATA_DIR}_${LASTMONTH}

 
