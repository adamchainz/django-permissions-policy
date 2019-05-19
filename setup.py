#!/usr/bin/env python
import re

from setuptools import setup


def get_version(filename):
    with open(filename, 'r') as fp:
        contents = fp.read()
    return re.search(r"__version__ = ['\"]([^'\"]+)['\"]", contents).group(1)


version = get_version('django_feature_policy.py')


with open('README.rst', 'r') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst', 'r') as history_file:
    history = history_file.read()

setup(
    name='django-feature-policy',
    version=version,
    description='Set the draft security HTTP header Feature-Policy on your Django app.',
    long_description=readme + '\n\n' + history,
    author='Adam Johnson',
    author_email='me@adamj.eu',
    url='https://github.com/adamchainz/django-feature-policy',
    py_modules=['django_feature_policy'],
    include_package_data=True,
    install_requires=[
        'Django>=1.11',
    ],
    python_requires='>=3.5',
    license='ISC',
    zip_safe=False,
    keywords='Django',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
