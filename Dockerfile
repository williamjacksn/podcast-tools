FROM python:3.7.4-alpine3.10

COPY requirements.txt /podcast-tools/requirements.txt

RUN /usr/local/bin/pip install --no-cache-dir --requirement /podcast-tools/requirements.txt

COPY . /podcast-tools

ENTRYPOINT ["/bin/sh"]

ENV PYTHONUNBUFFERED 1

LABEL org.opencontainers.image.authors="William Jackson <william@subtlecoolness.com>" \
      org.opencontainers.image.source="https://github.com/williamjacksn/podcast-tools" \
      org.opencontainers.image.version=2.0.4
