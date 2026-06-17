import os
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    return os.getenv(name, str(default)).lower() in {"1", "true", "yes", "on"}


def env_list(name, default=""):
    raw_value = os.getenv(name, default)
    return [item.strip() for item in raw_value.split(",") if item.strip()]


def _django_build_command_running():
    if len(sys.argv) < 2:
        return False
    return sys.argv[1] in {"collectstatic", "migrate", "check"}


is_render = os.environ.get("RENDER", "").lower() == "true"
is_railway = bool(
    os.environ.get("RAILWAY_ENVIRONMENT")
    or os.environ.get("RAILWAY_PROJECT_ID")
    or os.environ.get("RAILWAY_PUBLIC_DOMAIN")
)
is_hosted = is_render or is_railway

_django_secret = (
    os.getenv("DJANGO_SECRET_KEY", "").strip()
    or os.getenv("SECRET_KEY", "").strip()
)
if _django_secret:
    SECRET_KEY = _django_secret
elif env_bool("DJANGO_DEBUG", not is_hosted) or _django_build_command_running():
    SECRET_KEY = "dev-only-change-me-before-deploy"
else:
    from django.core.exceptions import ImproperlyConfigured

    raise ImproperlyConfigured(
        "Set DJANGO_SECRET_KEY when DJANGO_DEBUG=false (production)."
    )

DEBUG = env_bool("DJANGO_DEBUG", not is_hosted)

_allowed_raw = os.getenv("DJANGO_ALLOWED_HOSTS") or os.getenv("ALLOWED_HOSTS")
if _allowed_raw:
    ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS") if os.getenv("DJANGO_ALLOWED_HOSTS") else env_list("ALLOWED_HOSTS")
else:
    ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

if is_railway:
    for _host in (".railway.app", ".up.railway.app", "healthcheck.railway.app"):
        if _host not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(_host)

for _env_name, _prefix in (
    ("RENDER_EXTERNAL_HOSTNAME", "https://"),
    ("RAILWAY_PUBLIC_DOMAIN", "https://"),
):
    _hostname = os.environ.get(_env_name, "").strip()
    if _hostname and _hostname not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(_hostname)

CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")
for _env_name in ("RENDER_EXTERNAL_HOSTNAME", "RAILWAY_PUBLIC_DOMAIN"):
    _hostname = os.environ.get(_env_name, "").strip()
    if _hostname:
        _origin = f"https://{_hostname}"
        if _origin not in CSRF_TRUSTED_ORIGINS:
            CSRF_TRUSTED_ORIGINS.append(_origin)

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'pages',
    'posts',
    'accounts',
    'crispy_forms',
    'crispy_bootstrap5',
    'rest_framework',
    'rest_framework_simplejwt',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'channels',
    'django_filters',
]

if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']

INTERNAL_IPS = ['127.0.0.1']

# Crispy Forms settings
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

# Django Allauth settings
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

# Render-friendly site/domain and social provider configuration.
SITE_DOMAIN = os.getenv("DJANGO_SITE_DOMAIN", "localhost:8000")
SITE_NAME = os.getenv("DJANGO_SITE_NAME", "Blog-2")


# Updated Allauth settings for Django 5.2+
ACCOUNT_LOGIN_METHODS = {'email', 'username'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'optional'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE.insert(2, 'debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# Channels layer (in-memory for dev)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

_database_url = os.environ.get("DATABASE_URL")
if _database_url:
    _db_kwargs = {"conn_max_age": 600}
    if _database_url.startswith("postgres://"):
        _database_url = "postgresql://" + _database_url[len("postgres://") :]
    if "railway.internal" in _database_url:
        if "sslmode=" not in _database_url:
            _database_url += "&sslmode=disable" if "?" in _database_url else "?sslmode=disable"
        _db_kwargs["ssl_require"] = False
    elif "railway" in _database_url:
        if "sslmode=" not in _database_url:
            _database_url += "&sslmode=require" if "?" in _database_url else "?sslmode=require"
        _db_kwargs["ssl_require"] = not DEBUG
    DATABASES["default"] = dj_database_url.parse(_database_url, **_db_kwargs)
    DATABASES["default"].setdefault("OPTIONS", {})
    DATABASES["default"]["OPTIONS"].setdefault("connect_timeout", 10)

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER', 'noreply@example.com')
CONTACT_EMAIL = os.getenv('CONTACT_EMAIL', 'dallas8000@gmail.com')

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': ['user:email'],
    },
}

SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True

SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'same-origin'
SESSION_COOKIE_SECURE = env_bool('DJANGO_SESSION_COOKIE_SECURE', not DEBUG)
CSRF_COOKIE_SECURE = env_bool('DJANGO_CSRF_COOKIE_SECURE', not DEBUG)
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST = True
    # Railway probes /health/ over plain HTTP inside the container — never redirect.
    SECURE_SSL_REDIRECT = False if is_railway else env_bool('DJANGO_SECURE_SSL_REDIRECT', True)
else:
    SECURE_SSL_REDIRECT = env_bool('DJANGO_SECURE_SSL_REDIRECT', False)

# Django REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

