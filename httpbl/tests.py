#coding: utf-8
from django.utils import unittest
from django.test.client import RequestFactory
from django.http import HttpResponseNotFound, HttpResponsePermanentRedirect

from httpbl.middleware import HttpBLMiddleware


class HttpBLMiddlewareTestCase(unittest.TestCase):
	def setUp(self):
		self.mw = HttpBLMiddleware()
		self.mw.age = 1
		self.mw.threat = 1
		self.mw.api_key = 'abcdefghijkl' # API key for testing purposes. You should probably use your own.
		self.mw.logging = False
		self.quicklink = 'http://google.com/'
		self.req = RequestFactory()

	def test_threat(self):
		"""
		This should redirect to QuickLink or return HttpResponseNotFound.
		"""
		self.mw.classification = 1
		req = self.req.get('/')
		req.environ['REMOTE_ADDR'] = '127.1.1.1'
		threat = self.mw.is_threat(req)
		self.assertTrue(threat)

		response = self.mw.process_request(req)
		self.assertIsInstance(response, HttpResponsePermanentRedirect)

		self.mw.quicklink = False
		response = self.mw.process_request(req)
		self.assertIsInstance(response, HttpResponseNotFound)

	def test_search_engine(self):
		"""
		This should allow the client in.
		"""
		self.mw.classification = 1
		req = self.req.get('/')
		req.environ['REMOTE_ADDR'] = '127.1.1.0'
		threat = self.mw.is_threat(req)
		self.assertFalse(threat)

		response = self.mw.process_request(req)
		self.assertEqual(response, None)


	def test_innocent(self):
		"""
		This should let the client in.
		"""
		self.mw.classification = 1
		req = self.req.get('/')
		req.environ['REMOTE_ADDR'] = '127.0.0.1'
		threat = self.mw.is_threat(req)
		self.assertFalse(threat)

		response = self.mw.process_request(req)
		self.assertEqual(response, None)


	def test_suspicious(self):
		"""
		This should let the client in setting 'httpbl_suspicious' context variable to True.
		"""
		self.mw.classification = 2
		req = self.req.get('/')
		req.environ['REMOTE_ADDR'] = '127.1.1.1'
		threat = self.mw.is_threat(req)
		self.assertFalse(threat)

		response = self.mw.process_request(req)
		self.assertEqual(response, None)

