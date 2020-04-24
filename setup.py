#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# flake8: noqa
from __future__ import print_function

import io
import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


def read(*names, **kwargs):
    return io.open(
        os.path.join(here, *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


about = {}
exec(read('src', 'pytest', '__version__.py'), about)
long_description = read('README.md')

setup(
    name='ironpython-pytest',
    description='Ridiculously minimal and incomplete pytest replacement for IronPython',
    url='https://github.com/gramaziokohler/ironpython-pytest',
    version=about['__version__'],
    license=about['__license__'],
    author=about['__author__'],
    author_email=about['__email__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: IronPython',
    ],
    keywords=['unit-testing'],
    packages=['pytest'],
    package_dir={'': 'src'},
    package_data={},
    data_files=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    python_requires='>=2.7',
    extras_require={},
    entry_points={},
    ext_modules=[],
    cmdclass={}
)
