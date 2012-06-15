#coding: utf-8
from django.db import models


class HttpBLLog(models.Model):
	ip = models.IPAddressField()
	datetime = models.DateTimeField(auto_now_add=True)
	user_agent = models.CharField(max_length=100)
	result = models.IPAddressField(help_text='Refer to http://www.projecthoneypot.org/httpbl_api.php for explanation.')

	def __unicode__(self):
		return "%s" % self.ip
