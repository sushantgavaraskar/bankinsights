# WSGI config for bankinsight_backend project
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bankinsight_backend.settings')

application = get_wsgi_application()
from whitenoise import WhiteNoise
application = WhiteNoise(application)
