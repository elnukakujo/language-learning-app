#!/bin/sh
# Manual deploy: run on PCT after `git pull`.
# Builds both images locally, imports them into k3s's containerd (no registry
# involved — single node, images never leave the machine), applies manifests,
# rolls out the cluster.
set -e

LAPP_PUBLIC_HOST=192.168.1.125
LAPP_PUBLIC_PORT=30080

cd "$(dirname "$0")/.."

docker build -t fluence-backend:test .
docker save fluence-backend:test | k3s ctr images import -

docker build -f client/Dockerfile \
  --build-arg LAPP_PUBLIC_HOST=$LAPP_PUBLIC_HOST \
  --build-arg LAPP_PUBLIC_PORT=$LAPP_PUBLIC_PORT \
  -t fluence-frontend:test .
docker save fluence-frontend:test | k3s ctr images import -

kubectl apply -f k8s/
kubectl -n fluence rollout restart deployment/backend deployment/frontend
kubectl -n fluence rollout status deployment/backend --timeout=90s
kubectl -n fluence rollout status deployment/frontend --timeout=60s
