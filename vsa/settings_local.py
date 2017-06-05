"""

"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# celery
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ANNOTATIONS = {'*': {'rate_limit': '500/s'}}



SECRET_KEY = 'fe=b)!m4c0o1!kal74tu2!n=9n33rr+lbn8u=ajpa$blegkptj'


DEBUG = True

# TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'server',
    'permission',
    'quicklink',
    'vcenter',
    'logs',
    'admanage',
    'bind',
    'idc',
    'live',
    'monitor',
    'notify',
    'assets',
    'resources',
    'configmanage',

]


MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]




ROOT_URLCONF = 'vsa.urls'

WSGI_APPLICATION = 'vsa.wsgi.application'


# Database


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vsa',
        'USER': 'vsa',
        'PASSWORD': 'nibuzhidao',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Internationalization


LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True





TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug' : True,
            'context_processors' : [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
            'libraries': {
                'vcenter': 'vcenter.templatetags.jsonfilters',
            },
        },
    },
]




# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.zhengjin99.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'xtyw@zhengjin99.com'
EMAIL_HOST_PASSWORD = 'ST\OGyb8Pp0P'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

DEPLOYUSER = 'deploy'


VCENTER = "10.99.12.10"
VCENTERUSER = "tao.song@zhengjin99.com"
VCENTERPASSWD = "St@19871224"

INTERNAL_IPS = ('127.0.0.1',)

BINDSERVERADDR = "10.99.12.13"


ZABBIX_URL = "http://172.16.33.10/api_jsonrpc.php"
ZABBIX_USER = "tao.song"
ZABBIX_PASSWD = "St@19871224"