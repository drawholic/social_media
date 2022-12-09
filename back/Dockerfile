FROM python:3.8.10


VOLUME ["/web"]

WORKDIR "/web"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY ./requirements.txt /web/requirements.txt

RUN pip install --no-cache-dir -r /web/requirements.txt

COPY . /web

EXPOSE 8080
