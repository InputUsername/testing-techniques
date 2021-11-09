#!/bin/sh

[ -d /data/media_store ] && rm -rf /data/media_store
[ -f /data/homeserver.db ] && rm -f /data/homeserver.db
mkdir /data/media_store
chmod -R 777 /data
python /start.py