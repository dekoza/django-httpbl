#coding: utf-8
from django.contrib import admin
from httpbl.models import HttpBLLog


class HttpBLLogAdmin(admin.ModelAdmin):
	"""
	TODO: Maybe add filtering by type?
	TODO: Maybe add search_fields?
	"""
	date_hierarchy = 'datetime'
	list_display = ('datetime', 'ip', 'result', 'user_agent')
	list_display_links = list_display
	readonly_fields = list_display


admin.site.register(HttpBLLog, HttpBLLogAdmin)
