#!/bin/sh
set -e
cp /packed/tools/diagnostics /operations/tools/
exec "$@"
