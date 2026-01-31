FROM python:3.11.5

ARG NODE_HOME=/usr/src/node

WORKDIR ${NODE_HOME}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

RUN apt-get update \
  && apt-get clean

COPY requirements ${NODE_HOME}/requirements

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements/dev.txt

COPY . ${NODE_HOME}

RUN chmod +x entrypoint.sh