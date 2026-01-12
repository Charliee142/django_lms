
from pathlib import Path
import os

from dotenv import load_dotenv
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') == 'True'

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.humanize',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'lmsapp',
    'blogapp',
    "crispy_forms",
    "crispy_bootstrap5",
    'django_countries',
    'django_social_share',

    "django.contrib.sites",  # 
    "allauth",  # new
    "allauth.account",  # new
    "allauth.socialaccount",  # new
    "allauth.socialaccount.providers.github",  # new for GitHub provider
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",  # new
]


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",  
    "allauth.account.auth_backends.AuthenticationBackend",  # new
]


ROOT_URLCONF = 'lmsproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':  [BASE_DIR / "lmsapp/templates", BASE_DIR / "blogapp/templates"],
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

WSGI_APPLICATION = 'lmsproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

#ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = None # This option allows you to set whether the email address should be verified to register
ACCOUNT_EMAIL_VERIFICATION = 'optional' # This option can be used to set whether an email verification is necessary for a user to log in after he registers an account. You can also set none to send no verification email. (Not Recommended)
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
#ACCOUNT_RATE_LIMITS  = 5 # The maximum number of login attempts can be set, and the user gets blocked from logging back in until a timeout
#ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT= 86400 # 1 day in seconds
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1 # Sets the number of days within which an account should be activated. 
#ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = None
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = False
#ACCOUNT_SESSION_REMEMBER = None
#ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
#ACCOUNT_TEMPLATE_EXTENSION = "html"
ACCOUNT_UNIQUE_EMAIL = True
#ACCOUNT_SIGNUP_FORM_CLASS = 'blog.forms.SignupForm'
#ACCOUNT_USER_MODEL_USERNAME_FIELD = True
ACCOUNT_EMAIL_NOTIFICATIONS = True


SITE_ID = 1
LOGIN_REDIRECT_URL = '/'  # default to /accounts/profile 
ACCOUNT_LOGOUT_REDIRECT_URL ='/accounts/login/'

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


STATIC_URL = '/static/'
STATICFILES_DIRS = [
   os.path.join(BASE_DIR, "static"),
   ]

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email settings
EMAIL_BACKEND ='django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'emails'

KEY_ID = os.getenv('RAZORPAY_PUBLIC_KEY')
KEY_SECRET = os.getenv('RAZORPAY_SECRET_KEY')

# card :  4718 6091 0820 4366
