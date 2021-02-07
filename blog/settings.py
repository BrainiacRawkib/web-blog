"""
Django settings for blog project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
import django_heroku
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG') == 'True')

ALLOWED_HOSTS = []

ADMINS = [
    (os.getenv('ADMIN'), os.getenv('EMAIL_HOST_USER')),
]

MANAGERS = ADMINS

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.postgres',
    'django_comments_xtd',
    'django_comments',

    # third party
    'tinymce',
    'taggit',
    'crispy_forms',
    'sorl.thumbnail',

    'posts.apps.PostsConfig',
    'users.apps.UsersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [Path.joinpath(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'brainiac1998',
        'HOST': 'localhost',
        'PORT': 5433
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# CSRF_COOKIE_SECURE = True

# SESSION_COOKIE_SECURE = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

CLOUDINARY_URL = os.getenv('CLOUDINARY_URL')

# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

STATIC_URL = '/static/'
STATIC_ROOT = Path.joinpath(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'blog/static')
]

MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'users:profile'
LOGOUT_REDIRECT_URL = 'posts:index'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

# email config
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = (os.getenv('EMAIL_USE_TLS') == 'True')

# django comments xtd config
COMMENTS_APP = 'django_comments_xtd'
COMMENTS_XTD_MODEL = 'posts.models.PostComment'
COMMENTS_XTD_LIST_ORDER = ('-thread_id', 'order')
COMMENTS_XTD_MAX_THREAD_LEVEL = 1

COMMENTS_XTD_SALT = (b"Timendi causa est nescire. "
                     b"Aequam memento rebus in arduis servare mentem.")

# Source mail address used for notifications.
COMMENTS_XTD_FROM_EMAIL = "noreply@example.com"

# Contact mail address to show in messages.
COMMENTS_XTD_CONTACT_EMAIL = "helpdesk@example.com"

COMMENTS_XTD_APP_MODEL_OPTIONS = {
    'posts.post': {
        'allow_flagging': True,
        'allow_feedback': True,
        'show_feedback': True,
        'who_can_post': 'users'
    }
}

# JAZZMIN Settings
JAZZMIN_SETTINGS = {
    # title of the window
    "site_title": "Tech Blog",

    # Title on the brand, and the login screen (19 chars max)
    "site_header": "Tech Blog",

    # square logo to use for your site, must be present in static files, used for favicon and brand on top left
    "site_logo": "img/favicon.jpg",

    # Welcome text on the login screen
    "welcome_sign": "Tech Blog",

    # Field name on user model that contains avatar image
    "user_avatar": 'img/linux.png',

    # Change view #
    "changeform_format": "carousel",
}

# TinyMCE Settings
TINYMCE_DEFAULT_CONFIG = {
    'height': 500,
    'width': 'auto',  # 1120
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    # 'theme': 'modern',
    'plugins': '''
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak emoticons
    ''',
    'toolbar1': '''
        fullscreen preview bold italic underline | fontselect,
        fontsizeselect  | forecolor backcolor | alignleft alignright |
        aligncenter alignjustify | indent outdent | bullist numlist table |
        | link image media | codesample | emoticons
        ''',
    'toolbar2': '''
        visualblocks visualchars |
        charmap hr pagebreak nonbreaking anchor |  code |
        ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
}
# TINYMCE_SPELLCHECKER = True

django_heroku.settings(locals())
