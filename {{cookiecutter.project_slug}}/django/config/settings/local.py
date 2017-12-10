"""
Local settings for {{cookiecutter.project_name}} project.
"""
from redis import ConnectionPool

from .base import *  # noqa

local_use_redis = not env.bool('LOCAL_USE_REDIS', default=False)

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY', default='CHANGEME!!!')

# DATABASE
DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres://postgres@127.0.0.1/{{cookiecutter.project_slug}}'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

if local_use_redis:
    CACHES["default"] = {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient", }
    }


# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

if local_use_redis:
    CACHES["default"] = {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient", }
    }

# HUEY
# ------------------------------------------------------------------------------

huey_always_eager = not env.bool('LOCAL_USE_REDIS', default=not DEBUG)

HUEY = {
    'name': DATABASES['default']['NAME'],  # Use db name for huey.
    'always_eager': True,  # If DEBUG=True, run synchronously.
}

if !DEBUG or local_use_redis:
    print("HUEY läuft nicht im always_eager mode!")
    HUEY = {
        'name': DATABASES['default']['NAME'],  # Use db name for huey.
        'always_eager': False,  # If DEBUG=True, run synchronously.
        'connection': {
            'connection_pool': ConnectionPool(host='localhost', port=6379, max_connections=20),
        },
        'consumer': { 'workers': 4, },
    }


# django-debug-toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
INSTALLED_APPS += ['debug_toolbar', ]

INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['django_extensions', ]

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Your local stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
