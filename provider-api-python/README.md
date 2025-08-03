# Provider API

Mock service implementation for event provider dependency replacement.

## Overview

HTTP API service that provides event data in XML format. Built with FastAPI for async performance and proper dependency injection patterns.

## Requirements

- Python 3.11+
- Poetry for dependency management

## Installation

```bash
poetry install
```

## Configuration

Environment variables or `.env` file:

```
HOST=0.0.0.0
PORT=8081
LOG_LEVEL=info
ENV=development
```

## Usage

Development:
```bash
poetry run uvicorn src.provider_api.main:app --reload --port 8081
```

Production:
```bash
poetry run uvicorn src.provider_api.main:app --host 0.0.0.0 --port 8081
```

Docker:
```bash
docker build -t provider-api .
docker run -d -p 8081:8081 --name provider-api provider-api
```

## Docker Operations

Build and run the containerized service:

```bash
# Build the Docker image
docker build -t provider-api .

# Run the container in detached mode
docker run -d -p 8081:8081 --name provider-api provider-api

# Check container status
docker ps

# View container logs
docker logs provider-api

# Stop and remove container
docker stop provider-api && docker rm provider-api
```

Health check commands:

```bash
# Basic service info
curl http://localhost:8081/

# Health status endpoint
curl http://localhost:8081/health

# Spring Boot compatible health check
curl http://localhost:8081/actuator/health

# Events endpoint (XML response)
curl http://localhost:8081/events
```

## API Endpoints

- `GET /health` - Service health status
- `GET /actuator/health` - Spring Boot compatible health check
- `GET /events` - Event data endpoint

## Testing

```bash
poetry run pytest
```

Unit tests cover request handlers and business logic. Integration tests verify service communication patterns.

## Architecture

Standard FastAPI application structure with separation of concerns:

- Configuration management via Pydantic Settings
- Structured logging with correlation tracking
- Docker multi-stage builds for production deployment
- Health checks for orchestration platforms

## Development

Code formatting:
```bash
poetry run black src/ tests/
poetry run isort src/ tests/
```

Type checking:
```bash
poetry run mypy src/
```

## Deployment

Service runs on port 8081 to avoid conflicts with existing services on 8080. Health endpoints support both custom monitoring and Spring Boot actuator patterns for infrastructure compatibility.

Container builds use multi-stage approach for optimized production images. Resource limits and security contexts configured for Kubernetes deployment.

## License

MIT
