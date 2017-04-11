import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='python-cards',
    version='1.3',
    url='https://github.com/mrlucascardoso/pycards',
    license='MIT License',
    author='Lucas Cardoso',
    author_email='mr.lucascardoso@gmail.com',
    keywords='creditcard',
    description='Set of classes for validating, identifying and formatting do credit cards and debit cards.',
    packages=find_packages(),
    install_requires=[],
    test_suite='tests',
    setup_requires=['pytest-runner', ],
    tests_require=['pytest', ],
    include_package_data=True,
    long_description=README,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
)