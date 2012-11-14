#! /bin/bash
date; nice -n 19 s3multiput -a AKIAJV5O63YWVSJ5F2QQ -s 4Ev19xSjqRA6GNOnOucp1222J7eziO6QVEpFWWHZ -b gqr-analytics-data-inbox -p /mnt/bigdiskA/TwitterData/Outbox -k TwitterSample/ -w $1; date;
