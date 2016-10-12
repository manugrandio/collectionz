#!/usr/bin/env python

from setuptools import setup

setup(
    name='collectionz',
    version='0.0.1',
    description=(
        'A set of utility data structures that could fit in the '
        '``collections`` package of Python\'s standard library.'),
    url='https://github.com/manugrandio/collectionz',
    author='Manu Grandío Bravo',
    maintainer='Manu Grandío Bravo',
    maintainer_email='manugrandio@fastmail.fm',
    license='BSD',
    keywords='utility collections',
    packages=['collectionz'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
