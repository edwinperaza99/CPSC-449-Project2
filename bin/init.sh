#!/bin/sh

sqlite3 ./var/primary/fuse/books.db < ./share/books.sql
