# encoding: utf-8
"""
    setup
    ~~~~~

    :copyright: 2014 by Daniel Neuhäuser
    :license: BSD, see LICENSE.rst for details
"""
from setuptools import setup


setup(
    name='oore',
    description='Object-Oriented Regular Expressions',
    version='0.1.0',
    author='Daniel Neuhäuser',
    author_email='ich@danielneuhaeuser.de',
    url='https://github.com/DasIch/oore',

    py_modules=['oore'],

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
