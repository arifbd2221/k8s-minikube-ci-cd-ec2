#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Get the last commit count as the version
VERSION=$(git rev-list --count HEAD)

# Build the Docker image with the commit count as the version tag
docker build -t "$DOCKER_USERNAME/$IMAGE_NAME:$VERSION" .

# Optionally, push the Docker image to DockerHub
docker push "$DOCKER_USERNAME/$IMAGE_NAME:$VERSION"

# Output the image tag for reference
echo "Docker image $DOCKER_USERNAME/$IMAGE_NAME:$VERSION built and pushed successfully."
