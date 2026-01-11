FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gcc libpq-dev \
 && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:/root/.cargo/bin:${PATH}"

RUN uv --version

COPY pyproject.toml uv.lock* /app/

RUN uv venv && (uv sync --frozen || uv sync)

COPY . /app

EXPOSE 8000

CMD ["sh", "-c", "uv run python manage.py migrate --noinput && (uv run python manage.py runapscheduler &) && exec uv run uvicorn core.asgi:application --host 0.0.0.0 --port 8000"]
