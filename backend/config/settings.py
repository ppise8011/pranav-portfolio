import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv
BASE_DIR=Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')
DEBUG=os.getenv('DEBUG','True').lower()=='true'
SECRET_KEY=os.getenv('SECRET_KEY','development-only-change-before-deploying')
if not DEBUG and (len(SECRET_KEY)<50 or SECRET_KEY.startswith('development-')):
 raise ImproperlyConfigured('Set a unique SECRET_KEY of at least 50 characters before production deployment.')
ALLOWED_HOSTS=[v.strip() for v in os.getenv('ALLOWED_HOSTS','localhost,127.0.0.1').split(',') if v.strip()]
CSRF_TRUSTED_ORIGINS=[v.strip() for v in os.getenv('CSRF_TRUSTED_ORIGINS','http://localhost:5173,http://127.0.0.1:5173').split(',') if v.strip()]
INSTALLED_APPS=['django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','portfolio']
MIDDLEWARE=['django.middleware.security.SecurityMiddleware','whitenoise.middleware.WhiteNoiseMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','portfolio.middleware.LoginThrottleMiddleware','django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF='config.urls'
WSGI_APPLICATION='config.wsgi.application'
TEMPLATES=[{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[],'APP_DIRS':True,'OPTIONS':{'context_processors':['django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]
if os.getenv('POSTGRES_DB'):
 DATABASES={'default':{'ENGINE':'django.db.backends.postgresql','NAME':os.environ['POSTGRES_DB'],'USER':os.getenv('POSTGRES_USER','portfolio'),'PASSWORD':os.getenv('POSTGRES_PASSWORD',''),'HOST':os.getenv('POSTGRES_HOST','127.0.0.1'),'PORT':os.getenv('POSTGRES_PORT','5432'),'CONN_MAX_AGE':60}}
else:
 DATABASES={'default':{'ENGINE':'django.db.backends.sqlite3','NAME':BASE_DIR/'db.sqlite3','OPTIONS':{'timeout':20}}}
AUTH_PASSWORD_VALIDATORS=[{'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},{'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator','OPTIONS':{'min_length':12}},{'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator'},{'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator'}]
LANGUAGE_CODE='en-us'
TIME_ZONE='Asia/Kolkata'
USE_I18N=True
USE_TZ=True
STATIC_URL='/static/'
STATIC_ROOT=BASE_DIR/'staticfiles'
MEDIA_URL='/media/'
MEDIA_ROOT=BASE_DIR/'media'
FRONTEND_DIST=BASE_DIR.parent/'frontend'/'dist'
WHITENOISE_ROOT=FRONTEND_DIST
STORAGES={'default':{'BACKEND':'django.core.files.storage.FileSystemStorage'},'staticfiles':{'BACKEND':'whitenoise.storage.CompressedManifestStaticFilesStorage'}}
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
DATA_UPLOAD_MAX_MEMORY_SIZE=16384
FILE_UPLOAD_MAX_MEMORY_SIZE=5*1024*1024
# Upload limits are additionally enforced by the image validator and production proxy.
SESSION_COOKIE_HTTPONLY=True
CSRF_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE='Lax'
SESSION_COOKIE_AGE=28800
SESSION_COOKIE_SECURE=not DEBUG
CSRF_COOKIE_SECURE=not DEBUG
SECURE_SSL_REDIRECT=not DEBUG
SECURE_HSTS_SECONDS=31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS=False
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_REFERRER_POLICY='strict-origin-when-cross-origin'
X_FRAME_OPTIONS='DENY'
if os.getenv('TRUST_PROXY','False').lower()=='true':
 SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO','https')
# Set only behind a proxy that overwrites X-Real-IP and blocks direct app access.
TRUST_PROXY=os.getenv('TRUST_PROXY','False').lower()=='true'
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST=os.getenv('EMAIL_HOST','')
EMAIL_PORT=int(os.getenv('EMAIL_PORT','587'))
EMAIL_HOST_USER=os.getenv('EMAIL_HOST_USER','')
EMAIL_HOST_PASSWORD=os.getenv('EMAIL_HOST_PASSWORD','')
EMAIL_USE_TLS=os.getenv('EMAIL_USE_TLS','True').lower()=='true'
EMAIL_TIMEOUT=8
DEFAULT_FROM_EMAIL=os.getenv('DEFAULT_FROM_EMAIL','portfolio@localhost')
INQUIRY_NOTIFY_EMAIL=os.getenv('INQUIRY_NOTIFY_EMAIL','pranavpise8011@gmail.com')
CSRF_FAILURE_VIEW='portfolio.views.csrf_failure'
