from django.conf import settings

DEBUG = getattr(settings, "DEBUG", False)
DJANGO_TABLES2_TEMPLATE = getattr(settings, "DJANGO_TABLES2_TEMPLATE", "django_tables2/bootstrap5.html")
DJBACKOFFICE_SHOW_USER_DJANGO = getattr(settings, "DJBACKOFFICE_SHOW_USER_DJANGO", True)
