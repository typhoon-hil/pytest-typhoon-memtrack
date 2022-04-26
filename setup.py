#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-typhoon-memtrack',
    version='1.0.0',
    author='Vanja Mijatov',
    author_email='vanja.mijatov@typhoon-hil.com',
    maintainer='Vanja Mijatov',
    maintainer_email='vanja.mijatov@typhoon-hil.com',
    license='MIT',
    url='https://github.com/typhoon-hil/pytest-typhoon-memtrack',
    description='A Typhoon HIL plugin that tracks resource consumption during test session at runtime',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    packages=['tytest.memtrack'],
    python_requires='>=3.6',
    install_requires=[
        'pytest>=6.2.5',
        'matplotlib>=3.0.0'
        ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'tytest = tytest.memtrack.plugin',
        ],
    },
)
