from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ub!8*e@^1p5zcbm7gu+wv_r+gij@jyi!-32y6n6+9rtxo=_yv$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'Notificacao',
    'Pagamento',
    'Partida',
    'User',

    'AutenticacaoGoogle',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'VolleiAPP.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'VolleiAPP.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]


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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'User.perfilUsuario'
LOGIN_REDIRECT_URL = '/accounts/profile/'
ACCOUNT_SIGNUP_REDIRECT_URL = '/accounts/profile/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/partidas/'  # Ou qualquer URL desejada
ACCOUNT_CHANGE_PASSWORD_REDIRECT_URL = '/accounts/profile/'  # Após alterar a senha

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# Backend padrão para envio de emails
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'                                # Servidor SMTP
EMAIL_PORT = 587                                             # Porta para envio
# Ativar TLS para segurança
EMAIL_USE_TLS = True
# Email usado para enviar mensagens
EMAIL_HOST_USER = 'python.para.programacao@gmail.com'
# Senha do email
EMAIL_HOST_PASSWORD = 'huen igjb ukqj mkck'


# Caminho para o diretório de mídia
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuração do static
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

load_dotenv()

STRIPE_TEST_PUBLIC_KEY = os.getenv('STRIPE_TEST_PUBLIC_KEY')
STRIPE_TEST_SECRET_KEY = os.getenv('STRIPE_TEST_SECRET_KEY')

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',  # Dados de perfil (nome, foto)
            'email',    # Dados de email
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',  # Pode ser 'offline' se precisar de token de atualização
        },
        'EXCHANGE_TOKEN': True,
        'VERIFIED_EMAIL': True,
        'APP': {
            'client_id': '610863815012-rciabfudhl8lj6f5qv4q07u8vqgh04p5.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    }
}
