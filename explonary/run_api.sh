#!/bin/bash
mkdir /static
cd /code/explonary
./manage.py migrate
./manage.py collectstatic --noinput

if [ "$1" == "release" ]; then
    uwsgi --http :8000 --chdir /code/explonary --wsgi-file /code/explonary/explonary/wsgi.py --master --processes 4 --threads 2
else
    ./manage.py update_category
    ./manage.py runserver 0.0.0.0:8000    
fi