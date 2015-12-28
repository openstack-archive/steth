#!/usr/bin/env python
from setuptools import setup, find_packages

PROJECT = 'stetho'

VERSION = '0.1'


try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='CLI for stetho',
    long_description=long_description,

    author='Zhi Chang',
    author_email='changzhi@unitedstack.com',

    url='https://github.com/changzhi1990/stetho.git',
    download_url='https://github.com/changzhi1990/stetho.git',

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['cliff'],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'stetho = stethoclient.shell:main'
        ]
    },
)
