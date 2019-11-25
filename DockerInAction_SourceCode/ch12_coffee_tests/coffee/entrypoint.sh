#!/bin/bash

n=0
until [ $n -ge 10 ]
do
  python manage.py create_tables && break
  n=$[$n+1]
  sleep 1
done

gunicorn -w 4 -b 0.0.0.0:3000 app.wsgi:app
