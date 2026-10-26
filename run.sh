#!/usr/bin/env sh

set -e

DOCKER_PATH=$(command -v docker)
IMAGE_NAME="ysoserial-env"

# Build the image only if it doesn't already exist
if ! "$DOCKER_PATH" image inspect "$IMAGE_NAME" >/dev/null 2>&1; then
    echo "Docker image not found. Building..."
    "$DOCKER_PATH" build -t "$IMAGE_NAME" .
fi

# Run the container, ensuring "$@" follows the target image name.
"$DOCKER_PATH" run --rm \
    -v "$PWD/ysoserial.py:/app/ysoserial.py:ro" \
    "$IMAGE_NAME" "$@"
