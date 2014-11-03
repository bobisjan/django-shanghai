import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-shanghai',
    version='0.0.5',
    packages=['shanghai'],
    license='MIT License',
    description='A Django app to provide JSON API resources.',
    long_description=README,
    url='https://github.com/bobisjan/django-shanghai',
    author='Jan Bobisud',
    author_email='me@bobisjan.com',
    test_suite='tests.runner.run_tests'
)
