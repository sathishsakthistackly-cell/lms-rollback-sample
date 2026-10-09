#!/usr/bin/env sh
# Usage: deploy-rollback.sh CONTAINER_NAME HEALTH_URL [PREVIOUS_IMAGE]
set -eu
CONTAINER_NAME="${1:?Container name required}"
HEALTH_URL="${2:?Health URL required}"
PREVIOUS_IMAGE="${3:-}"
ATTEMPTS="${HEALTH_ATTEMPTS:-12}"
SLEEP_SECONDS="${HEALTH_SLEEP_SECONDS:-5}"
i=1
while [ "$i" -le "$ATTEMPTS" ]; do
  if curl --fail --silent "$HEALTH_URL" >/dev/null 2>&1; then
    echo "Health check passed on attempt $i."
    exit 0
  fi
  echo "Health check $i/$ATTEMPTS failed; waiting ${SLEEP_SECONDS}s..."
  sleep "$SLEEP_SECONDS"
  i=$((i + 1))
done
echo "Health check failed. Container logs:"
docker logs "$CONTAINER_NAME" || true
if [ -n "$PREVIOUS_IMAGE" ]; then
  echo "Rolling back to $PREVIOUS_IMAGE"
  docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
  docker run -d --name "$CONTAINER_NAME" --restart unless-stopped \
    -p "${HOST_PORT:-8080}:5000" "$PREVIOUS_IMAGE"
else
  echo "No previous image found; removing failed container."
  docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
fi
exit 1
