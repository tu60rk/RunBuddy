#!/bin/sh

while true; do
    pg_dump -h db -U ${DB_USER} -F c ${DB} -p ${DB_PORT} > "/opt/backup/last.sql"
    sleep 86400
done