from django.conf import settings
from django.http import HttpResponseNotFound, HttpResponsePermanentRedirect
import socket

class HttpBLMiddleware(object):
   """
   "HttpBL" Middleware by iamtgc@gmail.com 
   """
   def __init__(self, age=None, threat=None, classification=None):
      if age is None:
         self.age = getattr(settings, 'HTTPBLAGE', 14)
      else:
         self.age = age
      if threat is None:
         self.threat = getattr(settings, 'HTTPBLTHREAT', 30)
      else:
         self.threat = threat
      if classification is None:
         self.classification = getattr(settings, 'HTTPBLCLASS', 7)
      else:
         self.classification = classification

   def process_request(self, request):

      if settings.HTTPBLKEY:
         ip = request.META.get('REMOTE_ADDR')
         iplist = ip.split('.')
         iplist.reverse()

         domain = 'dnsbl.httpbl.org'

         query = settings.HTTPBLKEY + "." + ".".join(iplist) + "." + domain
            
         try:
            result = socket.gethostbyname(query)
         except socket.gaierror:
            return None

         resultlist = result.split('.')

         if (int(resultlist[1]) <= self.age and int(resultlist[2]) >= self.threat and int(resultlist[3]) & self.classification > 0):
            if settings.HTTPBLREDIRECT:
               return HttpResponsePermanentRedirect(settings.HTTPBLREDIRECT)
            else:
               return HttpResponseNotFound('<h1>Not Found</h1>')

      return None
