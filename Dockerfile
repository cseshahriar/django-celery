FROM python:3.11.4-alpine

WORKDIR /usr/src/app

# prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# ensure Python output is sent directly to the terminal without buffering
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# These paths are now relative to the build context, which is the project root (where this Dockerfile resides)
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# This copies everything else from the build context (the project root)
# into /usr/src/app in the container. This includes the 'django_celery' subdirectory.
COPY . /usr/src/app/

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]