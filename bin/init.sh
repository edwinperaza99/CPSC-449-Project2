#!/bin/sh

sqlite3 ./var/primary/fuse/classes.db < ./share/classes.sql
sqlite3 ./var/primary/fuse/users.db < ./share/users.sql