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

Information is logged using Pythons' built-in logging library. Subscribe to the logger `httpbl` to see requests being blocked or marked as suspicious.

Settings
--------

Please refer to http://www.projecthoneypot.org/httpbl_api.php to fine tune your settings.

* HTTPBL_KEY is a string containing your API Key from Project Honeypot.
* HTTPBL_QUICKLINK is a string containing your QuickLink. This is optional but you are strongly encouraged to use it as it helps catch new spammers.

Host will be identified as spammer and blocked if:

* the request method is not in `HTTPBL_IGNORE_REQUEST_METHODS` (default empty tuple); you could for example always allow `GET` requests, and block `POST` (and other) requests.
* the number of days since it was last seen in a honeypot is lower than value of `HTTPBL_AGE` (default 14)
* and host's threat score is greater than value of `HTTPBL_THREAT` (default 30)
* and host's classification bitset contains the bitset set in `HTTPBL_CLASS` (default 7).

For example if you want to block only Harversters and Comment Spammers but let in all Suspicious hosts,
you should set your HTTPBL_CLASS to 6.

Advanced Usage
--------------

By default spammers will be greeted with a somewhat cryptic `Page Not Found` message. Some spammers might be legit customers of your website you don't want to lock out. You could put extra anti-spam measures to still allow those visitors to use your website. This is where the `api` module can help.

This is an example of including a ReCAPTCHA for suspicious visitors on your website. Note that you need `django-recaptcha` and **disable the middleware**.

    # forms.py
    def get_form_class(request):
        if is_suspicious(request.META.get('REMOTE_ADDR')):
            return ContactFormWithCaptcha
        else:
            return ContactForm


    class ContactForm(forms.Form):
        name = forms.CharField(max_length=100)
        email = forms.EmailField(max_length=100)
        message = forms.CharField(max_length=2000, widget=forms.Textarea)


    class ContactFormWithCaptcha(ContactForm):
        captcha = ReCaptchaField()


TODO
----

* Write better tests.
* Add more context variables?

