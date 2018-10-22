FROM python:3.7.0-alpine3.8

COPY requirements-docker.txt /make-podcast/requirements-docker.txt

RUN /usr/local/bin/pip install --no-cache-dir --requirement /make-podcast/requirements-docker.txt

COPY . /make-podcast

ENTRYPOINT ["/usr/local/bin/python"]
CMD ["/make-podcast/make_podcast.py"]

ENV PYTHONUNBUFFERED 1

LABEL maintainer=william@subtlecoolness.com \
      org.label-schema.schema-version=1.0 \
      org.label-schema.version=1.0.1
