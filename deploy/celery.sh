#!/bin/sh
cd /code
celery -A testcode worker -l error