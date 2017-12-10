from redis import ConnectionPool

from .base import *  # noqa

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY')

# DATABASE
DATABASES = {
    'default': env.db('DATABASE_URL'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    "BACKEND": "django_redis.cache.RedisCache",
    "LOCATION": "redis://127.0.0.1:6379/1",
    "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient", }
}

# HUEY
# ------------------------------------------------------------------------------
HUEY = {
    'name': DATABASES['default']['NAME'],  # Use db name for huey.
    'always_eager': False,  # If DEBUG=True, run synchronously.
    'connection': {
        'connection_pool': ConnectionPool(host='localhost', port=6379, max_connections=20),
    },
    'consumer': { 'workers': 4, },
}
