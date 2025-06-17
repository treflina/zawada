from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-sxsip!ge$x3)8bf3*yh(@rp4&q_pgw7lmi%=45!2p2b@5+5uku"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass

INSTALLED_APPS += ["django_browser_reload",]

MIDDLEWARE += [
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]
