#!/bin/bash
cd /code/footimo
./manage.py migrate
./manage.py test
