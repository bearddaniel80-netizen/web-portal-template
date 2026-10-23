import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def read_secret(name: str) -> str:
    path = f"/run/secrets/{name}"

    if os.path.exists(path):
        return Path(path).read_text().strip()

    # Useful for local development outside Docker
    return os.environ[name]

# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------

SECRET_KEY = read_secret("django_secret_key")

DEBUG = os.environ.get("DJANGO_DEBUG", "false").lower() == "true"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "DJANGO_ALLOWED_HOSTS",
        "localhost,127.0.0.1",
    ).split(",")
    if host.strip()
]


# ---------------------------------------------------------------------------
# Applications
# ---------------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "mozilla_django_oidc",

    "portal",
]

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    
    # settings.py: add right after SecurityMiddleware
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "config.urls"


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"

ASGI_APPLICATION = "config.asgi.application"


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DATABASE_DB"],
        "USER": os.environ["DATABASE_USER"],
        "PASSWORD": os.environ["DATABASE_PASSWORD"],
        "HOST": os.environ.get("DATABASE_HOST", "db"),
        "PORT": os.environ.get("DATABASE_PORT", "5432"),
    }
}


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

AUTHENTICATION_BACKENDS = [
    "mozilla_django_oidc.auth.OIDCAuthenticationBackend",

    # Preserve Django's normal authentication for admin accounts
    # and other explicitly permitted local authentication.
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]

# Redirect unauthenticated users to authentik through OIDC.
LOGIN_URL = "oidc_authentication_init"
LOGIN_REDIRECT_URL_FAILURE = "/admin/login/"
LOGIN_REDIRECT_URL = "/"

LOGOUT_REDIRECT_URL = "/"

# ---------------------------------------------------------------------------
# authentik / OpenID Connect
# ---------------------------------------------------------------------------

AUTHENTIK_BASE_URL = os.environ.get(
    "AUTHENTIK_BASE_URL",
    "https://auth.example.com",
).rstrip("/")

AUTHENTIK_APPLICATION_SLUG = os.environ.get(
    "AUTHENTIK_APPLICATION_SLUG",
    "django-portal",
)
AUTHENTIK_INTERNAL_URL = "http://authentik-server:9000"
OIDC_OP_TOKEN_ENDPOINT = f"{AUTHENTIK_INTERNAL_URL}/application/o/token/"
OIDC_OP_USER_ENDPOINT  = f"{AUTHENTIK_INTERNAL_URL}/application/o/userinfo/"
OIDC_OP_JWKS_ENDPOINT  = f"{AUTHENTIK_INTERNAL_URL}/application/o/{AUTHENTIK_APPLICATION_SLUG}/jwks/"

OIDC_RP_SIGN_ALGO = "RS256"

OIDC_RP_CLIENT_ID = os.environ["OIDC_RP_CLIENT_ID"]

OIDC_RP_CLIENT_SECRET = read_secret(
    "authentik_oidc_client_secret"
)

OIDC_OP_AUTHORIZATION_ENDPOINT = (
    f"{AUTHENTIK_BASE_URL}/application/o/authorize/"
)

OIDC_OP_TOKEN_ENDPOINT = (
    f"{AUTHENTIK_BASE_URL}/application/o/token/"
)

OIDC_OP_USER_ENDPOINT = (
    f"{AUTHENTIK_BASE_URL}/application/o/userinfo/"
)

OIDC_OP_JWKS_ENDPOINT = (
    f"{AUTHENTIK_BASE_URL}/application/o/"
    f"{AUTHENTIK_APPLICATION_SLUG}/jwks/"
)

OIDC_RP_SCOPES = "openid email profile"

# Do not automatically create portal accounts for every identity
# that can authenticate with authentik.
OIDC_CREATE_USER = False

# Verify token signatures and TLS certificates.
OIDC_VERIFY_JWT = True
OIDC_VERIFY_SSL = True

# Require HTTPS for the OIDC callback in production.
# Your existing SECURE_PROXY_SSL_HEADER supports this behind Caddy.

# ---------------------------------------------------------------------------
# Internationalization
# ---------------------------------------------------------------------------

LANGUAGE_CODE = "en-us"

TIME_ZONE = os.environ.get(
    "DJANGO_TIME_ZONE",
    "America/New_York",
)

USE_I18N = True

USE_TZ = True


# ---------------------------------------------------------------------------
# Static files
# ---------------------------------------------------------------------------

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# ---------------------------------------------------------------------------
# Service Manager
# ---------------------------------------------------------------------------

NODE_URL = os.environ.get(
    "NODE_URL",
    "http://node:4000",
)

# ---------------------------------------------------------------------------
# Reverse proxy / HTTPS
# ---------------------------------------------------------------------------

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)


# ---------------------------------------------------------------------------
# Session security
# ---------------------------------------------------------------------------

SESSION_COOKIE_SECURE = not DEBUG

SESSION_COOKIE_HTTPONLY = True

SESSION_COOKIE_SAMESITE = "Lax"


# ---------------------------------------------------------------------------
# CSRF security
# ---------------------------------------------------------------------------

CSRF_COOKIE_SECURE = not DEBUG

CSRF_COOKIE_HTTPONLY = False

CSRF_COOKIE_SAMESITE = "Lax"


# ---------------------------------------------------------------------------
# Browser security
# ---------------------------------------------------------------------------

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "DENY"


# ---------------------------------------------------------------------------
# HSTS
#
# Enable after HTTPS is confirmed to be working correctly.
# ---------------------------------------------------------------------------

SECURE_HSTS_SECONDS = int(
    os.environ.get(
        "DJANGO_HSTS_SECONDS",
        "0",
    )
)

SECURE_HSTS_INCLUDE_SUBDOMAINS = (
    SECURE_HSTS_SECONDS > 0
)

SECURE_HSTS_PRELOAD = (
    SECURE_HSTS_SECONDS > 0
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        "django.request": {"handlers": ["console"], "level": "ERROR"},
        "mozilla_django_oidc": {"handlers": ["console"], "level": "DEBUG"},
    },
}