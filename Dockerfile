FROM python:3.7.2-alpine3.9

COPY requirements.txt /make-podcast/requirements.txt

RUN /usr/local/bin/pip install --no-cache-dir --requirement /make-podcast/requirements.txt

COPY . /make-podcast

ENTRYPOINT ["/usr/local/bin/python"]
CMD ["/make-podcast/make_podcast.py"]

ENV PYTHONUNBUFFERED 1

LABEL maintainer=william@subtlecoolness.com \
      org.label-schema.schema-version=1.0 \
      org.label-schema.version=2.0.2
