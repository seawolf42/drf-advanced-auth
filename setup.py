import os

from setuptools import find_packages
from setuptools import setup


try:
    with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
        README = readme.read()
except Exception:
    README = '<failed to open README.md>'


os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


install_dependencies = (
    'Django>=1.11',
)

test_dependencies = (
    'mock',
    'djangorestframework',
)


setup(
    name='drf_advanced_auth',
    version='0.2.3',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='Full authentication and credential management for Django REST Framework',
    long_description=README,
    long_description_content_type='text/markdown',
    author='jeffrey k eliasen',
    author_email='jeff+drf-advanced-auth@jke.net',
    url='https://github.com/seawolf42/drf-advanced-auth',
    zip_safe=False,
    keywords='drf-advanced-auth',
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=install_dependencies,
    tests_require=install_dependencies + test_dependencies,
    test_suite='runtests.run_tests',
)
