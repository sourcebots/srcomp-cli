from setuptools import find_namespace_packages, setup

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='sr.comp.cli',
    version='1.7.0',
    project_urls={
        'Documentation': 'https://srcomp-cli.readthedocs.org/',
        'Code': 'https://github.com/PeterJCLaw/srcomp-cli',
        'Issue tracker': 'https://github.com/PeterJCLaw/srcomp-cli/issues',
    },
    packages=find_namespace_packages(exclude=('docs*', 'script*', 'tests*')),
    namespace_packages=['sr', 'sr.comp'],
    description=(
        "Command line tools for interacting with the state of the Student "
        "Robotics Competition"
    ),
    long_description=long_description,
    author="Student Robotics Competition Software SIG",
    author_email='srobo-devel@googlegroups.com',
    install_requires=[
        'python-dateutil >=2.2, <3',
        'Fabric >= 2.7, <3',
        'invoke >= 1.7, <2',
        'sr.comp >=1.8, <2',
        'reportlab >=3.1.44, <3.7',
        'requests >=2.5.1, <3',
        'ruamel.yaml >=0.15, <1.0',
        'mido >=1.1, <2',
        'tabulate >=0.8.9, <0.10',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'srcomp = sr.comp.cli.command_line:main',
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
    ],
)
