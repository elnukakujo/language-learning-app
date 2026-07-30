#!/bin/sh
# Manual deploy: run on PCT after `git pull`.
# Images are built with Docker, imported into k3s's containerd, then the Docker
# copy is removed immediately — the Docker image only lives long enough to pipe
# it into containerd.
#
# To avoid disk-pressure (the machine holds ~one copy of the app, not two),
# backend/frontend are scaled to zero before the build. Old containerd images
# are pruned while nothing is running, then new images are imported and the
# deployments are re-applied to bring them back. Postgres is left running
# throughout — downtime is limited to the app tier.
set -e

cd "$(dirname "$0")/.."
. ./.env

# ── Docker garbage collection ───────────────────────────────────────────────
docker system prune -af

# ── Scale down app tier (postgres stays up) ─────────────────────────────────
kubectl -n fluence scale deployment/backend deployment/frontend --replicas=0
kubectl -n fluence wait --for=delete pod -l app=backend --timeout=120s || true
kubectl -n fluence wait --for=delete pod -l app=frontend --timeout=120s || true

# Force-delete any pods that survive the graceful wait
for deploy in backend frontend; do
  kubectl -n fluence get pods -l app=$deploy --no-headers 2>/dev/null | \
    awk '{print $1}' | \
    xargs -r kubectl -n fluence delete pod --force --grace-period=0 --wait=false
done || true

# Now safe: no app containers are running, all containerd images are eligible
# for pruning.
crictl rmi --prune 2>/dev/null || true

# ── Build & import backend ──────────────────────────────────────────────────
docker build -t fluence-backend:test .
docker save fluence-backend:test | k3s ctr --namespace=k8s.io images import -
docker rmi fluence-backend:test

# ── Build & import frontend ─────────────────────────────────────────────────
docker build -f client/Dockerfile \
  --build-arg LAPP_PUBLIC_HOST=$LAPP_PUBLIC_HOST \
  --build-arg LAPP_PUBLIC_PORT=$LAPP_PUBLIC_PORT \
  -t fluence-frontend:test .
docker save fluence-frontend:test | k3s ctr --namespace=k8s.io images import -
docker rmi fluence-frontend:test

# ── Bring the app tier back ─────────────────────────────────────────────────
# kubectl apply restores replicas:1 from the manifest; rollout restart ensures
# a fresh ReplicaSet even if the manifest didn't change.
kubectl apply -f k8s/
kubectl -n fluence rollout restart deployment/backend deployment/frontend
kubectl -n fluence rollout status deployment/backend --timeout=120s
kubectl -n fluence rollout status deployment/frontend --timeout=90s

# Final containerd cleanup (old untagged images from this deploy cycle).
crictl rmi --prune 2>/dev/null || true
