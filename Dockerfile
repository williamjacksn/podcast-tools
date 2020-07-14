FROM python:3.8.4-alpine3.12

COPY requirements.txt /podcast-tools/requirements.txt

RUN /usr/local/bin/pip install --no-cache-dir --requirement /podcast-tools/requirements.txt

COPY . /podcast-tools

ENTRYPOINT ["/bin/sh"]

ENV APP_VERSION="2.0.5" \
    PYTHONUNBUFFERED="1"

LABEL org.opencontainers.image.authors="William Jackson <william@subtlecoolness.com>" \
      org.opencontainers.image.source="https://github.com/williamjacksn/podcast-tools" \
      org.opencontainers.image.version="${APP_VERSION}"
