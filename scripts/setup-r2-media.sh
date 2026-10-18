#!/usr/bin/env bash
# Create R2 bucket, upload portfolio videos, attach media.ekkehardpetzold.de (optional).
# Requires: CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID
# Optional: CLOUDFLARE_ZONE_ID (zone for ekkehardpetzold.de on your Cloudflare account)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

BUCKET="${R2_BUCKET_NAME:-portfolio-ep-media}"
MEDIA_HOST="${MEDIA_HOSTNAME:-media.ekkehardpetzold.de}"
LOCATION="${R2_LOCATION:-weur}"

if [[ -z "${CLOUDFLARE_API_TOKEN:-}" || -z "${CLOUDFLARE_ACCOUNT_ID:-}" ]]; then
  echo "Set CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID." >&2
  exit 1
fi

export CLOUDFLARE_API_TOKEN CLOUDFLARE_ACCOUNT_ID

WRANGER=(npx wrangler)

echo "==> Wrangler account"
"${WRANGER[@]}" whoami

echo "==> Create bucket (idempotent): ${BUCKET} (${LOCATION})"
if ! "${WRANGER[@]}" r2 bucket list | grep -q "${BUCKET}"; then
  "${WRANGER[@]}" r2 bucket create "${BUCKET}" --location "${LOCATION}"
fi

echo "==> Upload video/*.mp4 to s3://${BUCKET}/video/"
shopt -s nullglob
files=(video/*.mp4)
if ((${#files[@]} == 0)); then
  echo "No files in video/ — nothing to upload." >&2
  exit 1
fi
for f in "${files[@]}"; do
  key="video/$(basename "$f")"
  echo "    ${key}"
  "${WRANGER[@]}" r2 object put "${BUCKET}/${key}" --file "$f" --content-type video/mp4 \
    --cache-control "public, max-age=31536000, immutable"
done

ZONE_ID="${CLOUDFLARE_ZONE_ID:-}"
if [[ -z "${ZONE_ID}" ]]; then
  echo "==> Looking up zone id for ekkehardpetzold.de (add site to Cloudflare if this fails)"
  ZONE_ID="$(curl -fsS -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
    "https://api.cloudflare.com/client/v4/zones?name=ekkehardpetzold.de&status=active" \
    | python3 -c "import sys,json; r=json.load(sys.stdin); print(r['result'][0]['id'] if r.get('result') else '')")"
fi

if [[ -n "${ZONE_ID}" ]]; then
  echo "==> Connect custom domain ${MEDIA_HOST} (zone ${ZONE_ID})"
  if ! "${WRANGER[@]}" r2 bucket domain list "${BUCKET}" 2>/dev/null | grep -q "${MEDIA_HOST}"; then
    "${WRANGER[@]}" r2 bucket domain add "${BUCKET}" --domain "${MEDIA_HOST}" --zone-id "${ZONE_ID}" -y
  fi
  echo ""
  echo "--- DNS (All-Inkl KAS) ---"
  echo "If Cloudflare does not auto-manage this record, add a CNAME for media → value shown below:"
  "${WRANGER[@]}" r2 bucket domain get "${BUCKET}" || true
else
  echo "==> No zone id — enable r2.dev for smoke test"
  "${WRANGER[@]}" r2 bucket dev-url enable "${BUCKET}" -y || true
  "${WRANGER[@]}" r2 bucket dev-url get "${BUCKET}" || true
  echo "Add ekkehardpetzold.de to Cloudflare (DNS can stay at All-Inkl), set CLOUDFLARE_ZONE_ID, re-run."
fi

echo ""
echo "Done. Public URLs: https://${MEDIA_HOST}/video/<filename>.mp4"
