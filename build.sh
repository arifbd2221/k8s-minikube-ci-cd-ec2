#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Log the current directory and list files
echo "Current directory: $(pwd)"
ls -al

# Get the last commit count as the version
VERSION=$(git rev-list --count HEAD)

# Log the version
echo "Version tag: $VERSION"

# Build the Docker image with the commit count as the version tag
docker build -t "$DOCKER_USERNAME/$IMAGE_NAME:$VERSION" .

# Optionally, push the Docker image to DockerHub
docker push "$DOCKER_USERNAME/$IMAGE_NAME:$VERSION"

# Output the image tag for reference
echo "Docker image $DOCKER_USERNAME/$IMAGE_NAME:$VERSION built and pushed successfully."
