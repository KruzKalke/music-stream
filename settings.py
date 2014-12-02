"""
Django settings for muse project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from djangoappengine.settings_base import *
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')
TEMPLATE_DIRS = [
	TEMPLATE_PATH,
]

AUTOLOAD_SITECONF = 'indexes'
#AUTHENTICATION_BACKENDS = ( 'django.contrib.auth.backends.ModelBackend')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!l$cfwjs1$n#&nrq&(7j1b-lfpft*%9j3q#b(exmerzdrod2hr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['.appspot.com']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'djangotoolbox',
    'autoload',
    'dbindexer',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'music_stream',
	'registration',
    'filetransfers',

    # djangoappengine should come last, so it can override a few manage.py commands
    'djangoappengine',
)

MIDDLEWARE_CLASSES = (

    # This loads the index definitions, so it has to come first
    'autoload.middleware.AutoloadMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
)

ROOT_URLCONF = 'muse.urls'

WSGI_APPLICATION = 'muse.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
# DATABASES['default'] = {'ENGINE': 'dbindexer', 'TARGET': DATABASES['default']}
DATABASES = {
    'default': {
        'ENGINE': 'dbindexer',
        'TARGET': 'gae',
    },
    'gae': {
        'ENGINE': 'djangoappengine.db',
    },
}

DBINDEXER_BACKENDS = (
    'dbindexer.backends.BaseResolver',
    'dbindexer.backends.FKNullFix',
    'dbindexer.backends.ConstantFieldJOINResolver',
)
# DATABASES = {
#     'default': {
#         'ENGINE': 'dbindexer',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

REGISTRATION_OPEN = True
ACCOUNT_ACTIVATION_DAYS = 10
REGISTRATION_AUTO_LOGIN = True
LOGIN_REDIRECT_URL = '/'
LOGIN_URL ='/accounts/login/'	

TEST_RUNNER = 'djangotoolbox.test.CapturingTestSuiteRunner'

ADMIN_MEDIA_PREFIX = '/media/admin/'
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

# STATIC_URL = '/static/'
# MEDIA_ROOT = '/path/to/myproject/media/'
# MEDIA_URL = '/media/'

STATIC_PATH = os.path.join(BASE_DIR,'static')

STATICFILES_DIRS = (
    STATIC_PATH,
)


MEDIA_PATH = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') 
MEDIA_URL = '/media/'

# PREPARE_UPLOAD_BACKEND = 'filetransfers.backends.default.prepare_upload'
# SERVE_FILE_BACKEND = 'filetransfers.backends.default.serve_file'
# PUBLIC_DOWNLOAD_URL_BACKEND = 'filetransfers.backends.default.public_download_url'