import os
import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Application definition

env = environ.Env()
env.read_env('.env')

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['ykrvil.com']

DATABASES = {
    'default': {
        'ENGINE': env.get_value('DATABASE_ENGINE'),
        'NAME': env.get_value('DATABASE_DB'),
        'USER': env.get_value('DATABASE_USER'),
        'PASSWORD': env.get_value('DATABASE_PASSWORD'),
        'HOST': env.get_value('DATABASE_HOST'),
        'PORT': env.get_value('DATABASE_PORT'),
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'moviebbs.apps.MoviebbsConfig', # 作成したアプリを追加
    'accounts.apps.AccountsConfig',
    'django.contrib.sites', # 追加
    'allauth', # 追加
    'allauth.account', # 追加
    'allauth.socialaccount', # 追加
    'allauth.socialaccount.providers.twitter', # 追加
    'allauth.socialaccount.providers.google', # 追加
    'bootstrap4', # 追加
]

# Bootstrap4 jqueryを使用するため追加
BOOTSTRAP4 = {
   'include_jquery': True,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
        os.path.join(BASE_DIR, 'templates'),
        os.path.join(BASE_DIR, 'templates', 'allauth'),
        ], # テンプレート用のフォルダを追記
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # Bootstrap4を使用するために追加
            'builtins': [
                'bootstrap4.templatetags.bootstrap4',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_NAME = os.path.basename(BASE_DIR)

STATIC_URL = '/static/'
STATIC_ROOT = '/usr/share/nginx/html/static' # 静的ファイルを集める場所（STATIC_ROOT）を指定
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] # 追加の静的ファイル探索パス

MEDIA_URL = '/media/'
MEDIA_ROOT = '/usr/share/nginx/html/media'


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 認証
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# sitesフレームワーク用のサイトID
SITE_ID = 1

# ログイン・ログアウト時のリダイレクト先
LOGIN_REDIRECT_URL = '/moviebbs/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'

#メールアドレスを確認しない
ACCOUNT_EMAIL_VERIFICATION = 'none'
