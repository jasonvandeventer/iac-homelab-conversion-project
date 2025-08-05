#!/usr/bin/env bash

if [ "$(id -u)" -eq 0 ]; then
  echo "⚠️ This script should not be run as root. Run without sudo."
  exit 1
fi

SERVICE=$1 # e.g. "sonarr"
ACTION=$2 # e.g. "deploy"

BASE_DIR=~/iac

if [[ -z "$SERVICE" || -z "$ACTION" ]]; then
  echo "Usage: $0 <service> <deploy|destroy|logs|status>"
  exit 1
fi

SERVICE_DIR="$BASE_DIR/$SERVICE"

case "$ACTION" in
  deploy)
    terraform -chdir="$SERVICE_DIR" init
    terraform -chdir="$SERVICE_DIR" apply -auto-approve
    ;;
  destroy)
    terraform -chdir="$SERVICE_DIR" destroy -auto-approve
    ;;
  logs)
    docker logs -f "$SERVICE"
    ;;
  status)
    curl -s "http://localhost:8989" >/dev/null && echo "$SERVICE is up" || echo "$SERVICE is down"
    ;;
  *)
    echo "Invalid action. Use deploy, destroy, logs, or status."
    exit 1
    ;;
esac
