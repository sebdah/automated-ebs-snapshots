""" Setup script for PyPI """
import configparser
import os
from setuptools import setup

settings = configparser.ConfigParser()
settings.read(os.path.realpath('automated_ebs_snapshots/settings.conf'))


setup(
    name='automated-ebs-snapshots',
    version=settings.get('general', 'version'),
    license='Apache License, Version 2.0',
    description='Automatic backup management of AWS EC2 EBS volumes',
    author='Sebastian Dahlgren, Skymill Solutions',
    author_email='sebastian.dahlgren@skymill.se',
    url='https://github.com/skymill/automated-ebs-snapshots',
    keywords="aws amazon web services ec2 ebs snapshot",
    platforms=['Any'],
    packages=['automated_ebs_snapshots'],
    scripts=['automated-ebs-snapshots'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['boto >= 2.29.1'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ]
)
