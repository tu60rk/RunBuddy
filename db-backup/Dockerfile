FROM postgres:13

COPY db-backup.sh /usr/local/bin/db-backup.sh
RUN chmod +x /usr/local/bin/db-backup.sh
COPY backup /usr/local/bin/backup
CMD ["db-backup.sh"]