#!/usr/bin/env bash
coverage run --branch --source=. ./manage.py test
coverage report
