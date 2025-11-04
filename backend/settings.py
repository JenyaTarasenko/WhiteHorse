





from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = 'django-insecure-kebt)bz_3v713tj-#$1^+tr56_7ep-@@&fmib5ay9@wy@nxfr3'


DEBUG = True
ALLOWED_HOSTS = ["*"]



INSTALLED_APPS = [
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'corsheaders',
    'rest_framework', #DRF
    'api.apps.ApiConfig', #app
    'rest_framework.authtoken',  # для токенов
    'djoser',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← обязательно 
    'django.contrib.sessions.middleware.SessionMiddleware',
    
     
    'django.middleware.locale.LocaleMiddleware',# LocaleMiddleware должен быть сразу после SessionMiddleware!
    
    'corsheaders.middleware.CorsMiddleware',#server для django react перед CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



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



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



STATIC_URL = 'static/'



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = [
    'localhost',
    '127.0.0.1',
]
###################

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
   
    "https://jenyatarasenko.pythonanywhere.com",# React
    
    
    
    'http://localhost:5173',
    'http://127.0.0.1:8001',

]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
