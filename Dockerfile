# Digest pin records the exact base reviewed by the security gate.
FROM python:3.12-alpine3.24@sha256:1b668429b3511ab407d8e00648891631b0b1a4d7e15e3ca70f38ab5b91ad4ab4
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1
RUN apk upgrade --no-cache && apk add --no-cache ffmpeg bash tzdata \
    && addgroup -g 10001 enat && adduser -D -H -u 10001 -G enat enat
WORKDIR /srv/enat
COPY requirements.lock ./
RUN python -m pip install --no-cache-dir --only-binary=:all: --require-hashes -r requirements.lock
# Verify the runtime graph, then remove the build-only package installer.
RUN python -m pip check && python -m pip uninstall -y pip
COPY app ./app
COPY migrations ./migrations
COPY scripts/run_api.sh ./scripts/run_api.sh
USER 10001:10001
EXPOSE 8000
CMD ["bash", "scripts/run_api.sh"]
