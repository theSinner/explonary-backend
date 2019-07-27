#!/bin/bash
cd /code/explonary
./manage.py migrate
./manage.py test
