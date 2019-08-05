#!/usr/bin/env bash

echo "removing database......"
echo "python3.6 manage.py flush"
python3.6 manage.py flush
echo "python3.6 manage.py sqlflush"
python3.6 manage.py sqlflush
echo "remove all migration files"
rm -f */migrations/00*
echo "remove database file"
rm -f db.sqlite3
echo "python3.6 manage.py makemigrations"
python3.6 manage.py makemigrations
echo "python3.6 manage.py migrate"
python3.6 manage.py migrate