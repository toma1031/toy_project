"""
Django settings for toy_project project.

Generated by 'django-admin startproject' using Django 2.2.17.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from datetime import timedelta
# ファイルの存在チェック用モジュール
import errno
# environをインポートして読み込む
import environ
env = environ.Env()
env.read_env('.env')
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# manage.pyと同じ階層に.envファイルを作り、そちらへ
# 必要な情報は格納する。そして下記のように呼び出す。
SECRET_KEY=env("SECRET_KEY")
EMAIL=env("EMAIL")
PASSWORD=env("PASSWORD")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

AUTH_USER_MODEL = 'accounts.User'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts',
    'find_retro_toys',
    'phone_field',
    'rest_framework',
    'rest_framework.authtoken', #追加
    'djoser', #追加
    'corsheaders', 
    # 投稿に紐づいたデータベースにある写真を消すため、下記を記載
    # 参考記事
    # https://pypi.org/project/django-cleanup/
    'django_cleanup.apps.CleanupConfig',
    # 検索機能
    'django_filters',

]


SIMPLE_JWT = {
    #トークンの時間を5分に設定
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    #暗号のアルゴリズム設定
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('JWT',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', #追加　（一番上に）

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.middleware.common.CommonMiddleware', # 追加
]

ROOT_URLCONF = 'toy_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'toy_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # 変更
        'NAME': 'toy_project', # プロジェクトで使用するデータベース名
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",
            },
        'USER': 'root', # パソコンにインストールしたMySQLのユーザー名
        'PASSWORD': '', # 同上。そのパスワード
        'PORT': 3306 
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'


JWT_AUTH = {
    'JWT_VERIFY_EXPIRATION': False,
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}

REST_FRAMEWORK = { 
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),  
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',　ここコメントアウト
        #Simple JWTを読み込む
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),  
    'NON_FIELD_ERRORS_KEY': 'detail',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    # 検索機能
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

# 追加
# Reactとの接続用（reactの開発用ポートが3000番のため）
CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
)

# MEDIA_ROOT は「ファイルを置く場所」であり、MEDIA_URLは「そのディレクトリの公開用のURL」です。
# ユーザーの投稿写真保存のファイルパス
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# 下記のコードは写真を保存して欲しいPathを設定
MEDIA_URL = '/media/'