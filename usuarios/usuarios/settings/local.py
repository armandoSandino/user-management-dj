# Cargar configuraciones del base.py
from .base import * 

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# mysql

DATABASES =  {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'usuarios_db',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}

# postgresql
'''
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'libro_db',
        'USER': 'armando',
        'PASSWORD': 'sandino',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
'''

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# Definir ruta para archivos estaticos, mi directorio se llamara 'static' ubicado en la raiz
STATICFILES_DIRS = [BASE_DIR.child('static')]

# Definir la ruta base para nuestros archivos multimedia
MEDIA_URL = '/media/'

# Definir la carpeta donde almacenamos los archivos multimedia
MEDIA_ROOT  = BASE_DIR.child('media')
