#!/usr/bin/env bash
set -x -e

DOCKER_COMPOSE_PREFIX=$(basename $(pwd))

### Tag the docker images
docker tag ${DOCKER_COMPOSE_PREFIX}_job_queue_flask_app quay.io/jerowe/job_queue_flask_app:latest


# Docker login
echo ${QUAY_API_TOKEN} | docker login quay.io -u jerowe  --password-stdin

# Push to quay
docker push quay.io/jerowe/job_queue_flask_app:latest
