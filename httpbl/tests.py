#coding: utf-8
from django.utils import unittest
from django.test.client import RequestFactory
from django.http import HttpResponseNotFound, HttpResponsePermanentRedirect
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

from httpbl.middleware import HttpBLMiddleware


class HttpBLMiddlewareTestCase(unittest.TestCase):
	def setUp(self):
		# prevent complaints about configuration if we only want to test the middleware
		if not getattr(settings, 'HTTPBL_KEY', False):
			setattr(settings, 'HTTPBL_KEY', 'abcdefghijkl') # This API key is legal ONLY for testing purposes.
		self.mw = HttpBLMiddleware()
		# Override other settings - we need a tight and consistent test case ;)
		self.mw.age = 1
		self.mw.threat = 1
		self.mw.classification = 1
		self.mw.logging = False
		self.quicklink = 'http://google.com/'
		self.req = RequestFactory().get('/')

	def test_config(self):
		if getattr(settings, 'HTTPBL_KEY', False):
			delattr(settings, 'HTTPBL_KEY')
		self.assertRaises(ImproperlyConfigured, HttpBLMiddleware)

	def test_threat(self):
		"""
		Detecting a threat should redirect to QuickLink or return HttpResponseNotFound.
		"""
		self.req.environ['REMOTE_ADDR'] = '127.1.1.1'
		threat = self.mw.is_threat(self.req)
		self.assertTrue(threat)

		response = self.mw.process_request(self.req)
		self.assertIsInstance(response, HttpResponsePermanentRedirect)

		self.mw.quicklink = False
		response = self.mw.process_request(self.req)
		self.assertIsInstance(response, HttpResponseNotFound)

	def test_search_engine(self):
		"""
		Search engines should be allowed.
		"""
		self.req.environ['REMOTE_ADDR'] = '127.1.1.0'
		threat = self.mw.is_threat(self.req)
		self.assertFalse(threat)

		response = self.mw.process_request(self.req)
		self.assertEqual(response, None)


	def test_innocent(self):
		"""
		Innocent hosts should be allowed.
		"""
		self.req.environ['REMOTE_ADDR'] = '127.0.0.1'
		threat = self.mw.is_threat(self.req)
		self.assertFalse(threat)

		response = self.mw.process_request(self.req)
		self.assertEqual(response, None)


	def test_suspicious(self):
		"""
		Depending on the settings some Suspicious hosts can be let in.
		In such cases 'httpbl_suspicious' context variable should be set to True.
		"""
		self.mw.classification = 2
		self.req.environ['REMOTE_ADDR'] = '127.1.1.1'
		threat = self.mw.is_threat(self.req)
		self.assertFalse(threat)

		response = self.mw.process_request(self.req)
		self.assertEqual(response, None)
