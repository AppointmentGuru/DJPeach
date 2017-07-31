#!/usr/bin/env bash
sleep 5
coverage run --branch --source=. ./manage.py test
coverage report
coverage xml
python-codacy-coverage -r coverage.xml
