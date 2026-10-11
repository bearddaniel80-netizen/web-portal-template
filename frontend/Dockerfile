# syntax=docker/dockerfile:1.7
# ---------- python-deps ----------
FROM python:3.12-slim AS deps

WORKDIR /build
 
COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install \
    --prefix=/install \
    -r requirements.txt

# -------- backend -----------------
FROM deps as runtime

COPY --from=deps /install /usr/local

WORKDIR /app

COPY src .

RUN python manage.py makemigrations

RUN python manage.py migrate

CMD ["uvicorn", "config.asgi:application",   "--host",  "0.0.0.0",  "--port",  "8000"]