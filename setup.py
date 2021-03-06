# coding=utf-8
from setuptools import setup, find_packages

setup(
    name='jzbutils',
    version='0.1.1',
    packages=find_packages(),
    exclude_package_date={'': ['.gitignore', 'test'],},
    author='chenglp',
    author_email='chenglongping@100tal.com',
    include_package_data=True,
    install_requires=['django<2.0', 'requests', 'django-cacheops'],
    description=''
)
