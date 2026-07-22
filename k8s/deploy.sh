#!/bin/sh
# Manual deploy: run on PCT after `git pull`.
# Builds both images locally, imports them into k3s's containerd (no registry
# involved — single node, images never leave the machine), applies manifests,
# rolls out the cluster.
set -e

cd "$(dirname "$0")/.."
. ./.env

docker build -t fluence-backend:test .
docker save fluence-backend:test | k3s ctr --namespace=k8s.io images import -

docker build -f client/Dockerfile \
  --build-arg LAPP_PUBLIC_HOST=$LAPP_PUBLIC_HOST \
  --build-arg LAPP_PUBLIC_PORT=$LAPP_PUBLIC_PORT \
  -t fluence-frontend:test .
docker save fluence-frontend:test | k3s ctr --namespace=k8s.io images import -

kubectl apply -f k8s/
kubectl -n fluence rollout restart deployment/backend deployment/frontend
kubectl -n fluence rollout status deployment/backend --timeout=90s
kubectl -n fluence rollout status deployment/frontend --timeout=60s

# prune old images & build cache AFTER rollout — doing it before deletes the
# newly imported images that aren't used by any container yet
docker image prune -f
docker builder prune -f
crictl rmi --prune 2>/dev/null || true
# Docker copy is dead weight once imported into containerd — keep only k3s copy
docker rmi fluence-backend:test fluence-frontend:test 2>/dev/null || true
