#!/usr/bin/env bash
# Quick tour of the IPAudit API — every endpoint, one curl each.
set -euo pipefail

IP="${1:-8.8.8.8}"
BASE="https://ipaudit.dev"

echo "== Full audit of $IP =="
curl -fsS "$BASE/api/analyze?ip=$IP" | python3 -m json.tool

echo
echo "== Your own IP (as seen by the API) =="
curl -fsS "$BASE/api/ip"

echo
echo "== Trust badge SVG saved to badge.svg =="
curl -fsS "$BASE/api/badge/$IP.svg?theme=dark" -o badge.svg
echo "badge.svg written"
