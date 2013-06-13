#coding: utf-8
from django.conf import settings
from django.http import HttpResponseNotFound, HttpResponsePermanentRedirect
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext as _
from httpbl.models import HttpBLLog
import socket


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
        self.classification = getattr(settings, 'HTTPBL_CLASS', 7)
        self.quicklink = getattr(settings, 'HTTPBL_QUICKLINK', False)
        self.logging = getattr(settings, 'HTTBL_LOG_BLOCKED', True)
        self.ignore_methods = getattr(settings, 'HTTPBL_IGNORE_REQUEST_METHODS', ())

    def is_threat(self, request):
        """
          Since I'm not quite sure if the same instance is used to process request and template response,
          I chose to leave the main part out.
          """
        if self.api_key:
            self.ip = request.META.get('REMOTE_ADDR')
            self.iplist = self.ip.split('.')
            self.iplist.reverse()

            domain = 'dnsbl.httpbl.org'

            query = self.api_key + "." + ".".join(self.iplist) + "." + domain

            try:
                self.result = socket.gethostbyname(query)
            except socket.gaierror:
                return False

            resultlist = self.result.split('.')

            self.suspicious = int(resultlist[3]) > 0

            if int(resultlist[3]) & self.classification > 0 and int(resultlist[1]) <= self.age and int(
                resultlist[2]) >= self.threat:
                return True
        return False

    def process_request(self, request):
        if request.method not in self.ignore_methods and self.is_threat(request):
            if self.logging:
                log = HttpBLLog(ip=self.ip, user_agent=request.META.get('HTTP_USER_AGENT'),
                                result=self.result)
                log.save()

            if self.quicklink:
                return HttpResponsePermanentRedirect(self.quicklink)
            else:
                return HttpResponseNotFound('<h1>Not Found</h1>')
        return None

    def process_template_response(self, request, response):
        if not self.is_threat(request):
            response.context_data['httpbl_suspicious'] = getattr(self, 'suspicious', False)
            response.context_data['httpbl_quicklink'] = getattr(self, 'quicklink', False)
        return response
