FROM alpine:3.15
RUN apk --no-cache add \
    python3
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"
WORKDIR /app
COPY pyproject.toml setup.cfg ./
RUN set -e; \
    mkdir src; \
    pip --no-cache-dir --disable-pip-version-check install -e .
COPY . ./
RUN pip --no-cache-dir --disable-pip-version-check install -e .
EXPOSE 80
ENTRYPOINT ["./docker-entrypoint.sh"]
