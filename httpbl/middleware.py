#coding: utf-8
from django.conf import settings
from django.http import HttpResponseNotFound, HttpResponsePermanentRedirect
from httpbl.models import HttpBLLog
import socket

class HttpBLMiddleware:
	"""
	"HttpBL" Middleware by iamtgc@gmail.com
	Modifications by dominik@kozaczko.info
	"""
	def __init__(self):
		self.age = getattr(settings, 'HTTPBL_AGE', 14)
		self.threat = getattr(settings, 'HTTPBL_THREAT', 30)
		self.classification = getattr(settings, 'HTTPBL_CLASS', 7)
		self.api_key = getattr(settings, 'HTTPBL_KEY', False)
		self.redirect = getattr(settings, 'HTTPBL_REDIRECT', False)
		self.logging = getattr(settings, 'HTTBL_LOG_BLOCKED', True)

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

			if int(resultlist[3]) & self.classification > 0 and int(resultlist[1]) <= self.age and int(resultlist[2]) >= self.threat:
				return True
		return False

	def process_request(self, request):
		if self.is_threat(request):
			if self.logging:
				log = HttpBLLog(ip = self.ip, user_agent = request.META.get('HTTP_USER_AGENT'), result = self.result)
				log.save()

			if self.redirect:
				return HttpResponsePermanentRedirect(settings.HTTPBL_REDIRECT)
			else:
				return HttpResponseNotFound('<h1>Not Found</h1>')
		else:
			return None


	def process_template_response(self, request, response):
		if not self.is_threat(request):
			response.context_data['httpbl_suspicious'] = getattr(self, 'suspicious', False)
			response.context_data['httpbl_quicklink'] =  getattr(settings, 'HTTPBL_REDIRECT', False)
		return response
