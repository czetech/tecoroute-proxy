#!/bin/sh
set -e

case $1 in

  ""|http)
    exec tecoroute-proxy
  ;;

  *)
    exec "$@"
  ;;

esac

exit 0
