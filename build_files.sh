#!/bin/bash

echo " BUILD START"
python3.9.1 -m ensurepip --upgrade
python3.9.1 -m pip install --upgrade pip setuptools 
python3.9.1 -m pip install django
python3.9.1 -m pip install psycopg2-binary
python3.9.1 -m pip install -r requirements.txt
python3.9.1 manage.py collectstatic --noinput --clear
echo " BUILD END"