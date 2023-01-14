FROM --platform=linux/amd64 python:3.10-slim-buster as base

# Celery does not work with root unless you force it
ENV C_FORCE_ROOT true

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

LABEL app.sample-app.image.name="crowdbotics-base"

# Install packages needed to run your application (not build deps):
# We need to recreate the /usr/share/man/man{1..8} directories first because
# they were clobbered by a parent image.
RUN set -ex \
    && RUN_DEPS=" \
        apt-utils \
        build-essential \
        nano \
        curl \
        inetutils-ping \
        libpcre3 \
        libtiff5-dev \
        zlib1g-dev \
        libpcre3 \
        libpcre3-dev \
        libjpeg62 \
        libjpeg62-turbo-dev \
        libfreetype6-dev \
        libwebp-dev \
        liblcms2-dev \
        libxml2-dev \
        libxslt-dev \
        python-dev \
        postgresql-client \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && apt-mark hold python2 python2-minimal python2.7 python2.7-minimal libpython2-stdlib libpython2.7-minimal libpython2.7-stdlib \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /project/code

# -----------------------------------------------------------------------------
FROM base AS development

LABEL app.sample-app.image.name="crowdbotics-development"

RUN set -ex \
    && RUN_DEPS=" \
        graphviz \
        graphviz-dev \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN set -ex \
    && pip3 install -I -U pip setuptools pipenv

COPY ./Pipfile ./Pipfile.lock /
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --dev --system

# -----------------------------------------------------------------------------
FROM base AS release

LABEL app.sample-app.image.name="crowdbotics-release"

ENV DEBUG=false

ARG USERNAME=docker
ARG UID=123
ARG GID=4567


RUN set -ex \
    && pip3 install -I -U pip setuptools pipenv

COPY ./conf/docker /project/conf
COPY ./Pipfile ./Pipfile.lock /
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --system --deploy --pre

RUN groupadd -r django \
  && useradd -d /opt/code/app -r -g django django \
  && chown django:django -R /opt/webapp
USER django

ENV PATH="/.venv/bin:$PATH"

COPY --chown=django:django . .

CMD ["/project/conf/services/waitress.sh"]

# -----------------------------------------------------------------------------
FROM release AS staging

LABEL app.sample-app.image.name="crowdbotics-staging"

# -----------------------------------------------------------------------------
FROM release AS production

LABEL app.sample-app.image.name="crowdbotics-production"