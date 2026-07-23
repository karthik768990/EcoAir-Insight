# Stage 1: Build dependencies
FROM python:3.11-slim as builder

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local

# Ensure local bin is in PATH
ENV PATH=/root/.local/bin:$PATH

# Copy backend app
COPY backend/app ./app

# Copy ML data processing (for migration script and CSVs)
COPY ml ./ml

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
