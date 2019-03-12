FROM python:3.7.2-alpine3.9

COPY requirements.txt /podcast-tools/requirements.txt

RUN /usr/local/bin/pip install --no-cache-dir --requirement /podcast-tools/requirements.txt

COPY . /podcast-tools

ENTRYPOINT ["/bin/sh"]

ENV PYTHONUNBUFFERED 1

LABEL maintainer=william@subtlecoolness.com \
      org.label-schema.schema-version=1.0 \
      org.label-schema.version=2.0.3
