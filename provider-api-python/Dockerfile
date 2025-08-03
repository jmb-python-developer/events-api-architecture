FROM python:3.11-slim AS base

WORKDIR /app

# Install dependencies directly
RUN pip install fastapi==0.104.1 \
    uvicorn[standard]==0.24.0 \
    pydantic==2.5.0 \
    pydantic-settings==2.1.0 \
    lxml==4.9.3 \
    httpx==0.25.2 \
    structlog==23.2.0

# Create app user
RUN adduser --disabled-password --gecos '' appuser
WORKDIR /app

# Copy application
COPY src/ ./src/
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8081

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8081/health')"

CMD ["python", "-m", "uvicorn", "src.provider_api.main:app", "--host", "0.0.0.0", "--port", "8081"]
