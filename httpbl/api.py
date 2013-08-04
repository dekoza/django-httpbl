import socket
from django.conf import settings

if not hasattr(settings, 'HTTPBL_KEY'):
    raise ImproperlyConfigured("Missing HTTPBL_KEY. Register on "
                               "http://projecthoneypot.org to get one.")

HTTPBL_KEY = getattr(settings, 'HTTPBL_KEY')
HTTPBL_AGE = getattr(settings, 'HTTPBL_AGE', 14)
HTTPBL_THREAT = getattr(settings, 'HTTPBL_THREAT', 30)
HTTPBL_CLASS = getattr(settings, 'HTTPBL_CLASS', 7)


def query(ip):
    query = '.'.join([HTTPBL_KEY] + ip.split('.')[::-1] + ['dnsbl.httpbl.org'])

    try:
        response = socket.gethostbyname(query)
    except socket.gaierror:
        return 0, 0, 0  # error is raised for non-spammy visitors

    error, age, threat, type_ = [int(x) for x in response.split('.')]

    assert error == 127, "Incorrect API Usage"

    return age, threat, type_


def is_threat(ip):
    age, threat, type_ = query(ip)
    return age < HTTPBL_AGE and threat > HTTPBL_THREAT and HTTPBL_CLASS & type_


def is_suspicious(ip):
    age, threat, type_ = query(ip)
    return type_ > 0
