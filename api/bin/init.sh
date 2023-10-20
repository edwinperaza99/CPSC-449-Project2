#!/bin/sh

sqlite3 ./api/var/primary/fuse/classes.db < ./api/share/classes.sql
# sqlite3 ./api/var/primary/fuse/users.ub   < ./api/share/users.sql