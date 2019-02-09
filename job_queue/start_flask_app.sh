#!/usr/bin/env bash

set -x -e

### hello
#./wait-for-it.sh -p 5672 -h rabbit
#gunicorn --workers=4 --bind=0.0.0.0:5000 --keep-alive=2000 --timeout=2000 --log-level=debug flask_app:app --daemon
#celery -A flask_app.celery worker --concurrency ${CELERY_INSTANCES}
#gunicorn --workers=4 --bind=0.0.0.0:5000 --keep-alive=2000 --timeout=2000 --log-level=debug flask_app:app
#celery flower -A proj --broker=${BROKER_URL} --address=0.0.0.0
