from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(DEBUG=(bool, False))
env.read_env(str(BASE_DIR / ".env"))

SECRET_KEY = env("SECRET_KEY")

DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = ["*"]


# Application definition
INSTALLED_APPS = [
    # Default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom apps
    'accounts',
    'establishments',

    # Third-party apps
    'phonenumber_field',
    'rest_framework',
    'django_redis',
    'corsheaders',
    'django_filters',
    'whitenoise',

    # Authentication apps
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'social_django',
]

MIDDLEWARE = [
    # Default middleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Third party middleware
    'corsheaders.middleware.CorsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'restaurants.urls'

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

WSGI_APPLICATION = 'restaurants.wsgi.application'

# Database for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Database for production
# DATABASES = {
#     'default': {
#         'ENGINE': env('DB_ENGINE', default='django.db.backends.mysql'),
#         'NAME': env('DB_NAME'),
#         'USER': env('DB_USER'),
#         'PASSWORD': env('DB_PASSWORD'),
#         'HOST': env('DB_HOST', default='localhost'),
#         'PORT': env.int('DB_PORT', default=3306),
#     }
# }

# Password validation
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
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images) and Media files (Images, Videos, etc.)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Static files storage using Whitenoise for production
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'accounts.User'

# Phone number field settings
PHONENUMBER_DB_FORMAT = 'VN'

# Email settings
EMAIL_HOST=env("EMAIL_HOST")
EMAIL_HOST_USER=env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD=env("EMAIL_HOST_PASSWORD")
EMAIL_PORT=env("EMAIL_PORT")
EMAIL_USE_TLS=env.bool("EMAIL_USE_TLS", default=True)
EMAIL_BACKEND=env("EMAIL_BACKEND")

# Cache settings
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{env('REDIS_HOST', default='127.0.0.1')}:{env('REDIS_PORT', default='6379')}/{env('REDIS_DB', default='1')}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# REST framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.linkedin.LinkedinOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

# Social authentication settings
# Google OAuth2 settings
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = env.list("SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE", default=[
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile"
])
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = env("SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI")

# Facebook OAuth2 settings
SOCIAL_AUTH_FACEBOOK_KEY = env("SOCIAL_AUTH_FACEBOOK_KEY")
SOCIAL_AUTH_FACEBOOK_SECRET = env("SOCIAL_AUTH_FACEBOOK_SECRET")
SOCIAL_AUTH_FACEBOOK_SCOPE = env.list("SOCIAL_AUTH_FACEBOOK_SCOPE", default=[
    "email", "public_profile"
])
SOCIAL_AUTH_FACEBOOK_REDIRECT_URI = env("SOCIAL_AUTH_FACEBOOK_REDIRECT_URI")

# LinkedIn OAuth2 settings
SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = env("SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY")
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = env("SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET")
SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = env.list("SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE", default=[
    "r_liteprofile", "r_emailaddress"
])
SOCIAL_AUTH_LINKEDIN_OAUTH2_REDIRECT_URI = env("SOCIAL_AUTH_LINKEDIN_OAUTH2_REDIRECT_URI")

# GitHub OAuth2 settings
SOCIAL_AUTH_GITHUB_KEY = env("SOCIAL_AUTH_GITHUB_KEY")
SOCIAL_AUTH_GITHUB_SECRET = env("SOCIAL_AUTH_GITHUB_SECRET")
SOCIAL_AUTH_GITHUB_REDIRECT_URI = env("SOCIAL_AUTH_GITHUB_REDIRECT_URI")
SOCIAL_AUTH_GITHUB_SCOPE = env.list("SOCIAL_AUTH_GITHUB_SCOPE", default=[
    "read:user", "user:email"
])

# Social authentication pipeline
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',

    # Custom pipeline
    'accounts.pipelines.check_existing_user',  
    'accounts.pipelines.create_user_if_not_exists',
)

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # for development only
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"]
CORS_ALLOW_HEADERS = ["*"]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173", # React app
]
# Cross-Origin-Opener-Policy (COOP) for cross-origin iframes
SECURE_CROSS_ORIGIN_OPENER_POLICY = None