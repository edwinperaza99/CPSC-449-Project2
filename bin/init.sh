#!/bin/sh

sqlite3 ./var/primary/fuse/books.db < ./share/books.sql
sqlite3 ./var/primary/fuse/users.db < ./share/users.sql