FROM continuumio/miniconda3:4.5.11

RUN apt-get update -y; apt-get upgrade -y
RUN apt-get install -y vim-tiny vim-athena ssh

## Intellij seems to need this to be able   to use docker-compose as a remote interpreter
#RUN conda update -y --all
#RUN conda install -y pip setuptools

RUN adduser --home /home/flask flask

USER flask
WORKDIR /home/flask

RUN mkdir -p job_queue_flask_app

WORKDIR /home/flask/job_queue_flask_app

COPY environment.yml environment.yml
RUN conda env create -f environment.yml
RUN echo "alias l='ls -lah'" >> ~/.bashrc
RUN echo "source activate job-queue" >> ~/.bashrc

ENV CONDA_EXE /opt/conda/bin/conda
ENV CONDA_PREFIX /home/flask/.conda/envs/job-queue
ENV CONDA_PYTHON_EXE /opt/conda/bin/python
ENV CONDA_PROMPT_MODIFIER (job-queue)
ENV CONDA_DEFAULT_ENV job-queue
ENV PATH /home/flask/.conda/envs/job-queue/bin:/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

COPY . ./
#CMD ["/bin/bash", "-c", "/home/flask/job_queue_flask_app/start_flask_app.sh"]
