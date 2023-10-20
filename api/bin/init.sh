#!/bin/sh

sqlite3 ./api/var/enrollments.db < ./api/share/enrollments.sql
sqlite3 ./api/var/primary/fuse/users.ub < ./api/share/users.sql