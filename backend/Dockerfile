# ── Stage 1: test & lint ────────────────────────────────────────────────────
FROM python:3.12-slim AS test

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Run lint (ruff) — fail build on lint errors
RUN ruff check .

# Run tests — fail build on test failures
RUN pytest --tb=short -q

# ── Stage 2: runtime ─────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
