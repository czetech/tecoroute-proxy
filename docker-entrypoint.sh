#!/bin/sh
set -e

entrypoint=tecoroute-proxy

if [ $# -eq 0 ]; then
  set -- $entrypoint
fi

if [ "${1:0:1}" = '-' ]; then
  set -- $entrypoint "$@"
fi

exec "$@"
