#coding: utf-8
import socket
import logging

from django.conf import settings
from django.http import HttpResponseNotFound, HttpResponsePermanentRedirect
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext as _
from .api import is_threat


logger = logging.getLogger(__name__)


class HttpBLMiddleware:
    """
     "HttpBL" Middleware by iamtgc@gmail.com
     Modifications by dominik@kozaczko.info
     """

    def __init__(self):
        self.quicklink = getattr(settings, 'HTTPBL_QUICKLINK', False)
        self.ignore_methods = getattr(settings, 'HTTPBL_IGNORE_REQUEST_METHODS', ())

    def process_request(self, request):
        ip = request.META.get('REMOTE_ADDR')

        if request.method not in self.ignore_methods and is_threat(ip):
            logger.warning('Blocked request from %s', ip)

            if self.quicklink:
                return HttpResponsePermanentRedirect(self.quicklink)
            else:
                return HttpResponseNotFound('<h1>Not Found</h1>')
