#!/bin/bash
mkdir /static
cd /code/explonary
celery -A explonary beat -l info