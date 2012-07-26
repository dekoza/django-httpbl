from distutils.core import setup

with open('README.md') as file:
    long_description = file.read()

setup(
    name='django-httpbl',
    long_description=long_description,
    version='0.1.20',
    packages=['httpbl'],
    url='https://github.com/dekoza/django-httpbl',
    license='BSD',
    author='Dominik Kozaczko',
    author_email='dominik@kozaczko.info',
    description='Django middleware implementing Http:BL API of projecthoneypot.org'
)
