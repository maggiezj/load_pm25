#!/bin/bash

PM25_DATA_DIR='/mydata/pm25'

LAST_MONTH=$(date -d "yesterday" +%Y%m)

mv -f ${PM25_DATA_DIR} ${PM25_DATA_DIR}_${LAST_MONTH}

 
