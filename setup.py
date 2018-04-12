# coding=utf-8
from setuptools import setup, find_packages

setup(
    name='jzbutils',
    version='0.1',
    packages=find_packages(),
    exclude_package_date={'': ['.gitignore', 'test'],},
    author='chenglp',
    author_email='chenglongping@100tal.com',
    include_package_data=True,
    install_requires=['django<=1.11', 'requests', 'django-cacheops==2.4.3'],
    description=''
)
