# coding: utf-8

from setuptools import setup, find_packages

setup(
    name = 'cross-connection',
    version = '0.2.8',
    packages = find_packages(exclude = ['test', 'docs', 'dist', 'build']),
    include_package_data=True,
    description = 'cross-connection library',
    author = 'Jie Meng',
    author_email='jiemeng@thoughtworks.com',
    license = 'Apache 2.0',
    install_requires = [
    ],
    entry_points = {
    },
)
