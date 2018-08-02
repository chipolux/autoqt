# -*- coding: utf_8 -*-
from setuptools import setup

from autoqt import VERSION


with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='autoqt',
    version=VERSION,
    description='Simplify pyqtProperty creation.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development',
    ],
    keywords='PyQt,PyQt5,pyqtProperty',
    author='NaKyle Wright',
    author_email='nakyle.wright@gmail.com',
    url='https://github.com/chipolux/autoqt/',
    py_modules=['autoqt'],
    python_requires='>=3.6',
    install_requires=[
        'PyQt5>=5.7.1',
    ],
)
