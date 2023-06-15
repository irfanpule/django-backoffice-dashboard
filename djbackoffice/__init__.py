__title__ = 'DJBackoffice'
__version__ = '0.0.1-alpha'
__author__ = 'irfanpule'


from django.utils.module_loading import autodiscover_modules
from djbackoffice.core import backoffice


def autodiscover():
    """
    autodiscover_modules all file backoffice.py to module
    """
    autodiscover_modules('backoffice', register_to=backoffice)
