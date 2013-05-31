#coding: utf-8
import socket
import logging

from django.conf import settings
from django.http import HttpResponseNotFound, HttpResponsePermanentRedirect
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext as _


logger = logging.getLogger(__name__)


class HttpBLMiddleware:
    """
     "HttpBL" Middleware by iamtgc@gmail.com
     Modifications by dominik@kozaczko.info
     """

    def __init__(self):
        self.api_key = getattr(settings, 'HTTPBL_KEY', False)
        if not self.api_key:
            raise ImproperlyConfigured(_("Missing HTTPBL_KEY. Register on http://projecthoneypot.org to get one."))
        self.age = getattr(settings, 'HTTPBL_AGE', 14)
        self.threat = getattr(settings, 'HTTPBL_THREAT', 30)
        self.type_ = getattr(settings, 'HTTPBL_CLASS', 7)
        self.quicklink = getattr(settings, 'HTTPBL_QUICKLINK', False)
        self.ignore_methods = getattr(settings, 'HTTPBL_IGNORE_REQUEST_METHODS', ())

    def is_threat(self, request):
        query = '.'.join([self.api_key] +
                         request.META.get('REMOTE_ADDR').split('.')[::-1] +
                         ['dnsbl.httpbl.org'])

        try:
            response = socket.gethostbyname(query)
        except socket.gaierror:
            return False  # error is raised for non-spammy visitors

        error, age, threat, type_ = [int(x) for x in response.split('.')]

        assert error == 127, "Incorrect API Usage"

        if age < self.age and threat >= self.threat and type_ & self.type_:
            logger.info('%s is a threat (age: %s, threat: %s, type=%s)',
                ip, age, threat, type_)
            return True
        elif type_ > 0:
            logger.info('%s is suspicious (age: %s, threat: %s, type=%s)',
                ip, age, threat, type_)

    def process_request(self, request):
        if request.method not in self.ignore_methods and self.is_threat(request):
            logger.warning('Blocked request from %s', request.META.get('REMOTE_ADDR'))

            if self.quicklink:
                return HttpResponsePermanentRedirect(self.quicklink)
            else:
                return HttpResponseNotFound('<h1>Not Found</h1>')
        return None
