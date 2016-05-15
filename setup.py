from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyKevo',

    version='1.0.0',

    url='https://github.com/jeremyforan/pyKevo',

    description='A simple Python project for people with Kevo smartlocks.',
    long_description=long_description,


    author='Jeremy Foran',
    author_email='jeremy.foran@gmail.com',

    license='Creative Commons Attribution-ShareAlike 3.0',

    classifiers=[

        'Intended Audience :: Developers',
        'Topic :: Home Automation',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='Kevo Smartlock Smartlocks',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=['requests'],

    entry_points={
        'console_scripts': [
            'pyKevo=pyKevo:main',
        ],
    },
)