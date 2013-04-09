__author__ = 'Andrew Hawker <andrew.r.hawker@gmail.com>'

import tcapy

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name=tcapy.__name__,
    version=tcapy.__version__,
    description='Python bindings for JetBrains TeamCity REST API.',
    long_description=open('README.md').read(),
    author='Andrew Hawker',
    author_email='andrew.r.hawker@gmail.com',
    url='https://github.com/ahawker/teamcity-apy',
    license=open('LICENSE.md').read(),
    package_dir={'tcapy': 'tcapy'},
    packages=['tcapy'],
    install_requires=['requests'],
    test_suite='tests',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    )
)
