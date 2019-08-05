#!/usr/bin/env bash


echo "python3.6 manage.py makemigrations"
python3.6 manage.py makemigrations
echo "python3.6 manage.py migrate"
python3.6 manage.py migrate