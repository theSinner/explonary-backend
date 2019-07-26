#!/bin/bash
mkdir /static
cd /code/explonary
celery worker -l info -A explonary