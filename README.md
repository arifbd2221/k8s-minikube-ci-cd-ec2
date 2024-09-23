# Django Application Deployment with Minikube on EC2 via GitHub Actions

This repository contains a Django REST API application deployed inside a Kubernetes cluster running on **Minikube**. The Minikube cluster is hosted on an **Amazon EC2** instance, and the system is configured to automatically build, tag, and deploy Docker images using **GitHub Actions**. The deployed service is accessed from the outside world using **Nginx**, which maps the EC2 public IP to Minikube's internal service IP.

## System Architecture Overview

1. **Django App**: A Django REST API deployed in a Minikube cluster.
2. **PostgreSQL Database**: The Django app connects to a PostgreSQL database, which is also hosted inside the Kubernetes cluster in Minikube.
3. **Kubernetes**: The Django app runs inside a Kubernetes pod in Minikube, which is hosted on an EC2 instance.
4. **Minikube**: Minikube is set up on EC2 to provide a local Kubernetes environment for running the Django app.
5. **Nginx**: Nginx runs on the EC2 instance and forwards traffic from the EC2 public IP to the Minikube internal service IP, making the Django API accessible externally.
6. **DockerHub**: Docker images for the Django app are stored in DockerHub, tagged with the latest commit number.
7. **GitHub Actions**: A CI/CD pipeline automatically builds and deploys the Docker image to Minikube on every push to the `main` branch.


## Docker Image Build and Tagging

The Docker image for the Django app is automatically built and tagged using the **latest commit number** from the repository. This commit number acts as the image version, ensuring that each build is unique. The image is then pushed to **DockerHub**, and from there, it is pulled into the EC2 instance for deployment in Minikube.


## Prerequisites

To replicate this system, ensure the following components are set up:

- An **Amazon EC2** instance (ensure you have SSH access).
- **Minikube** installed and running on the EC2 instance.
- **PostgreSQL** deployed inside the Minikube cluster for the Django service.
- **DockerHub** account to store and pull Docker images.
- **Nginx** installed on the EC2 instance, configured to route traffic to Minikube.
- **GitHub Secrets** configured for DockerHub credentials, EC2 SSH key, EC2 host, and other required secrets.

## Workflow Overview

### Nginx Configuration

Nginx is configured on the EC2 instance to map the public EC2 IP to the internal Minikube service IP. This allows external access to the service hosted within Minikube.

Sample Nginx configuration:

```nginx
server {
    listen 80;
    server_name YOUR_EC2_PUBLIC_IP;

    location / {
        proxy_pass http://YOUR_MINIKUBE_SERVICE_IP:PORT;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
