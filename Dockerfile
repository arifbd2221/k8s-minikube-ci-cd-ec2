# Use the lightweight Python 3.12 Alpine image
FROM python:3.12-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    curl

# Install pip and Poetry
RUN pip install --upgrade pip && pip install poetry

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock /app/

# Install project dependencies
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Copy the project files
COPY . /app/
COPY run_server.sh /run_server.sh
COPY wait-for-it.sh /wait-for-it.sh

# Install bash
RUN apk add --no-cache bash

RUN chmod +x /wait-for-it.sh
# Give execution permissions to the run script
RUN chmod +x /run_server.sh

# Run the server with the provided script
CMD ["/run_server.sh"]
