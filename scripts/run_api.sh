#!/usr/bin/env bash
set -euo pipefail
trusted_proxy_ips="${TRUSTED_PROXY_IPS:-127.0.0.1}"
if [[ "$trusted_proxy_ips" == *"*"* ]]; then
  echo "TRUSTED_PROXY_IPS must contain explicit proxy addresses" >&2
  exit 1
fi
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}" \
  --no-access-log \
  --proxy-headers --forwarded-allow-ips "$trusted_proxy_ips" \
  --limit-concurrency 100 --timeout-keep-alive 5 --timeout-graceful-shutdown 30
