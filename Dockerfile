FROM python:3.10.4-alpine3.15

RUN /usr/sbin/adduser -g python -D python

USER python
RUN /usr/local/bin/python -m venv /home/python/venv

ENV APP_VERSION="2021.2" \
    PATH="/home/python/venv/bin:${PATH}" \
    PYTHONUNBUFFERED="1"

COPY --chown=python:python requirements.txt /home/python/podcast-tools/requirements.txt
RUN /home/python/venv/bin/pip install --no-cache-dir --requirement /home/python/podcast-tools/requirements.txt

COPY --chown=python:python download_podcast.py /home/python/podcast-tools/download_podcast.py
COPY --chown=python:python make_podcast.py /home/python/podcast-tools/make_podcast.py

WORKDIR /home/python/podcast-tools
ENTRYPOINT ["/bin/sh"]

LABEL org.opencontainers.image.authors="William Jackson <william@subtlecoolness.com>" \
      org.opencontainers.image.source="https://github.com/williamjacksn/podcast-tools" \
      org.opencontainers.image.version="${APP_VERSION}"
