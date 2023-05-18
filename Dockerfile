FROM alpine:3.15
RUN apk --no-cache add \
    libuv \
    python3
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"
WORKDIR /app
COPY pyproject.toml setup.cfg ./
RUN set -e; \
    mkdir src; \
    apk --no-cache add -t build-tools gcc libc-dev make python3-dev; \
    pip --no-cache-dir --disable-pip-version-check install -e .[uvloop]; \
    apk --no-cache del build-tools
COPY . ./
RUN pip --no-cache-dir --disable-pip-version-check install -e .[uvloop]
EXPOSE 80
ENTRYPOINT ["./docker-entrypoint.sh"]
