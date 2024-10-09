
# define an alias for the specific python version used in this file.
FROM docker.io/python:3.12.7-slim-bookworm AS python

# Python build stage
FROM python AS python-build-stage

ARG BUILD_ENVIRONMENT=production

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg dependencies
  libpq-dev \
  wait-for-it

# Copying the lock file for Python dependencies
COPY ./requirements.lock .

# Installing dependencies and creating wheels
RUN pip install --no-cache-dir --no-index --no-deps --upgrade pip \
  && pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.lock



# Python 'run' stage
FROM python AS python-run-stage

# Setting build environment and application home directory
ARG BUILD_ENVIRONMENT=production
ARG APP_HOME=/app
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}
WORKDIR ${APP_HOME}


# Installing dependencies from previously created wheels
RUN --mount=type=bind,from=python-build-stage,source=/app/wheels,target=/wheels \
  pip install --no-cache --no-cache-dir --no-index --no-deps --find-links=/wheels/ /wheels/*  && \
  addgroup --system django && \
  adduser --system --ingroup django django



# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  # psycopg dependencies
  libpq-dev \
  # Translations dependencies
  gettext \
  wait-for-it \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY --chown=django:django ./docker/django/entrypoint /entrypoint
COPY --chown=django:django ./docker/django/start /start

RUN sed -i 's/\r$//g' /entrypoint \
  && chmod +x /entrypoint \
  && sed -i 's/\r$//g' /start \
  && chmod +x /start


# copy application code to WORKDIR

# Copying application source code, gunicorn configuration, and pyproject.toml
COPY --chown=django:django src ${APP_HOME}/src
COPY --chown=django:django manage.py ${APP_HOME}/manage.py

# make django owner of the WORKDIR directory as well.
RUN chown -R django:django ${APP_HOME}

USER django

RUN DATABASE_URL="" \
  CELERY_BROKER_URL="" \
  DJANGO_SETTINGS_MODULE="config.settings.test" \
  python manage.py compilemessages

ENTRYPOINT ["/entrypoint"]
CMD ["/start"]
