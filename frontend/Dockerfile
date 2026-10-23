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

# RUN python manage.py makemigrations portal
# RUN python manage.py migrate
# RUN python manage.py createsuperuser
# RUN python manage.py seed_portal
RUN django_secret_key=build-only \
    authentik_oidc_client_secret=build-only \
    DATABASE_DB=build DATABASE_USER=build DATABASE_PASSWORD=build \
    OIDC_RP_CLIENT_ID=build \
    python manage.py collectstatic --noinput

CMD ["sh", "-c", "python manage.py migrate && uvicorn config.asgi:application --host 0.0.0.0 --port 8000"]

#CMD ["uvicorn", "config.asgi:application",   "--host",  "0.0.0.0",  "--port",  "8000"]