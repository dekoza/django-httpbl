#coding: utf-8
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


class HttpBLLog(models.Model):
	ip = models.IPAddressField(_('IP'))
	datetime = models.DateTimeField(_('Datetime'), auto_now_add=True)
	user_agent = models.CharField(_('User Agent'), max_length=100)
	result = models.IPAddressField(_('Result'), help_text=mark_safe(_('Refer to <a href="http://www.projecthoneypot.org/httpbl_api.php">HttpBL API</a> for explanation.')))

	def __unicode__(self):
		return _("Blocked IP %(ip)s") % {'ip': self.ip}
