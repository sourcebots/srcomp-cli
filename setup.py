import sys

from setuptools import find_packages, setup


with open('README.rst') as f:
    long_description = f.read()

install_requires = [
    'python-dateutil >=2.2, <3',
    'paramiko >=1.10, <3',
    'sr.comp >=1.0, <2',
    'reportlab >=3.1.44, <3.5',
    'requests >=2.5.1, <3',
    'ruamel.yaml >=0.13.0, <0.16',
    'simplejson >=3.6, <4',
    'six >=1.9, <2',
    'Pillow >=2.7, <7',
    'mido >=1.1, <2'
]

if sys.version_info < (3, 4):
    install_requires.append('pathlib >=1.0, <2')

setup(
    name='sr.comp.cli',
    version='1.0.1',
    packages=find_packages(exclude=('tests',)),
    namespace_packages=['sr', 'sr.comp'],
    description='CLI tools for srcomp repositories',
    long_description=long_description,
    author='Student Robotics Competition Software SIG',
    author_email='srobo-devel@googlegroups.com',
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'srcomp = sr.comp.cli.command_line:main'
        ]
    },
    setup_requires=[
        'Sphinx >=1.3, <2'
    ],
    tests_require=[
        'mock >=1.0.1',
        'nose >=1.3, <2',
        'freezegun >=0.3, <0.4',
    ],
    test_suite='nose.collector'
)
