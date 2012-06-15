django-httpbl
=============

Django middleware implementing Http:BL API of projecthoneypot.org

This is a fork of http://code.google.com/p/django-httpbl-middleware/ originally by iamtgc. It needs a little update to Django 1.4.

Usage
-----

Prior to installing this middleware you should join http://projecthoneypot.org/ and get your API Key.

* Copy httpbl to your project's directory (sorry, no installer yet).
* Add 'httpbl' to INSTALLED_APPS.
* Insert 'httpbl.middleware.HttpBLMiddleware' into MIDDLEWARE_CLASSES list in your settings.
* Finetune your settings.

There will be some context variables available, so you can additionally fine tune your templates to handle suspicious hosts, for example enabling CAPTCHAs or turning off POST for such clients.

These context variables are:
* 'httpbl_suspicious' if the host passed the test but was marked as suspicious.
* 'httpbl_quicklink' is simply the URL you put in your settings (no need for separate templatetag then ;)

Settings
--------

Please refer to http://www.projecthoneypot.org/httpbl_api.php to fine tune your settings.

* HTTPBL_KEY is a string containing your API Key from Project Honeypot.
* HTTPBL_QUICKLINK is a string containing your QuickLink. This is optional but you are strongly encouraged to use it as it helps catch new spammers.
* If you do NOT want to log all blocked hosts you should set HTTPB_BL to False (default: True)

Host will be identified as spammer and blocked if:
* the number of days since it was last seen in a honeypot is lower than value of HTTPBL_AGE (default 14)
* and host's threat score is greater than value of HTTPBL_THREAT (default 30)
* and host's classification bitset contains the bitset set in HTTPBL_CLASS (default 7).

For example if you want to block only Harversters and Comment Spammers but let in all Suspicious hosts,
you should set your HTTBL_CLASS to 6.

TODO
----

* Write some tests.
* Add more context variables?
* Write an installer.

