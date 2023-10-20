#!/bin/sh

sqlite3 ./api/var/enrollments.db < ./api/share/enrollments.sql
sqlite3 ./api/var/primary/fuse/users.db < ./api/share/users.sql