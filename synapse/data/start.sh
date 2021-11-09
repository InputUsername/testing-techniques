#!/bin/sh

[ -d /data/media_store ] && rm -rf /data/media_store
[ -f /data/homeserver.db ] && rm -f /data/homeserver.db
python /start.py