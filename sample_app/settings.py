import django


DEBUG = True
USE_TZ = True

SECRET_KEY = 'abcdefghijklmnopqrstuvwxyz'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite',
    }
}

ROOT_URLCONF = 'sample_app.urls'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'sample_app',
)

SITE_ID = 1

_middleware_list = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

if django.VERSION >= (1, 10):
    MIDDLEWARE = _middleware_list
else:
    MIDDLEWARE_CLASSES = _middleware_list

TEMPLATES = (
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (),
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
)

AUTH_USER_MODEL = 'sample_app.CustomUser'

APPEND_SLASH = True
STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'sample_app.authentication.CsrfExemptSessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    )
}


LOGIN_REDIRECT_URL = 'index'


DRF_ADVANCED_AUTH = {
    'AUTH_TOKEN_LIFETIME_MINUTES': 15,
    'LOGIN_SUCCESS_RESPONSE_SERIALIZER': None,
}
