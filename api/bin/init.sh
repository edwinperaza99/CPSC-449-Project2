#!/bin/sh

sqlite3 ./api/var/primary/fuse/classes.db < ./api/share/classes.sql
