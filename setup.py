import os

from setuptools import setup, find_packages

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(DIR_PATH, 'README.md')) as file:
    long_description = file.read()

install_requires = [line.rstrip('\n') for line in open(os.path.join(DIR_PATH, 'requirements.txt'))]

setup(
    name='dmt',
    version='0.1.5',
    packages=find_packages(),
    author='kedod',
    author_email='kedod@protonmail.com',
    description='dmt',
    long_description=long_description,
    include_package_data=True,
    install_requires=install_requires,
    package_data={
        '': ['*.yaml']
    }
)
