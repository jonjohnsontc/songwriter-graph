# !/bin/bash
# Creates a backup of db and uploads it to Backblaze

TIME_AT_RUN=$(date +%Y%m%d) 
pg_dump -d postgres -U postgres -h localhost -f "${TIME_AT_RUN}_dump.sql" || true
b2 upload-file swg-db-dump ./${TIME_AT_RUN}_dump.sql ${TIME_AT_RUN}_dump.sql || true 
