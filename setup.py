""" Setup script for PyPI """
import os
from setuptools import setup
from ConfigParser import SafeConfigParser

settings = SafeConfigParser()
settings.read(os.path.realpath('automated_ebs_snapshots/settings.conf'))


setup(
    name='automated-ebs-snapshots',
    version=settings.get('general', 'version'),
    license='Apache License, Version 2.0',
    description='Automatic provisioning for AWS DynamoDB tables',
    author='Sebastian Dahlgren',
    author_email='sebastian.dahlgren@gmail.com',
    url='http://sebdah.github.com/dynamic-dynamodb/',
    keywords="dynamodb aws provisioning amazon web services",
    platforms=['Any'],
    packages=['automated_ebs_snapshots'],
    scripts=['automated-ebs-snapshots'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['boto >= 2.23.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ]
)
