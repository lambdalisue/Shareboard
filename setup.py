#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = "0.1.4"

def read(filename):
    import os.path
    return open(os.path.join(os.path.dirname(__file__), filename)).read()
setup(
    name="shareboard",
    version=version,
    description = "A local HTTP server based clipboard like pipe",
    long_description=read('README.md'),
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords = "http clipboard pipe cui viewer",
    author = "Alisue",
    author_email = "lambdalisue@hashnote.net",
    url=r"https://github.com/lambdalisue/reqviewer",
    download_url = r"https://github.com/lambdalisue/reqviewer/tarball/master",
    license = 'MIT',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    scripts = ['scripts/shareboard'],
    include_package_data = True,
    zip_safe = True,
    install_requires=['setuptools', 'requests'],
)
