# from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from djbackoffice.core import backoffice, BackofficeOptions
from djbackoffice.settings import DJBACKOFFICE_SHOW_USER_DJANGO


class UserBackofficeOpts(BackofficeOptions):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email',)


if DJBACKOFFICE_SHOW_USER_DJANGO:
    backoffice.register(get_user_model(), UserBackofficeOpts)
    backoffice.register(Group)
