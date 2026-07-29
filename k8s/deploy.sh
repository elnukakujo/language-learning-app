#!/bin/sh
# Manual deploy: run on PCT after `git pull`.
# Images are built with Docker, imported into k3s's containerd, then the Docker
# copy is removed immediately — the Docker image only lives long enough to pipe
# it into containerd. This keeps peak disk usage at ~one image, not two.
set -e

cd "$(dirname "$0")/.."
. ./.env

# Free space before building. Storage is tight (app fits exactly once, not
# twice). Previous deploys leave behind dangling images, BuildKit cache
# (including the uv cache mount with ~2.6GB of torch packages), and stopped
# containers — all dead weight once imported into containerd.
docker system prune -af

# --- backend ---
docker build -t fluence-backend:test .
docker save fluence-backend:test | k3s ctr --namespace=k8s.io images import -
docker rmi fluence-backend:test

# --- frontend ---
docker build -f client/Dockerfile \
  --build-arg LAPP_PUBLIC_HOST=$LAPP_PUBLIC_HOST \
  --build-arg LAPP_PUBLIC_PORT=$LAPP_PUBLIC_PORT \
  -t fluence-frontend:test .
docker save fluence-frontend:test | k3s ctr --namespace=k8s.io images import -
docker rmi fluence-frontend:test

kubectl apply -f k8s/
kubectl -n fluence rollout restart deployment/backend deployment/frontend
kubectl -n fluence rollout status deployment/backend --timeout=90s
kubectl -n fluence rollout status deployment/frontend --timeout=60s

# Containerd prune after rollout — before rollout the old images are still in
# use by running containers, and the new images aren't used by any container yet
# (would get deleted).
crictl rmi --prune 2>/dev/null || true
