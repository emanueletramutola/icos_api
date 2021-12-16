#!/usr/bin/env python

import io
from os import path
import setuptools

app_name = 'icos'

__version__ = '1.0.0'


def read(f_name):
    file_path = path.join(path.dirname(__file__), f_name)
    return io.open(file_path, encoding='utf-8').read()


setuptools.setup(
    name=app_name,
    version=__version__,
    description=read('README.md'),
    author="CNR IMAA",
    author_email="emanuele.tramutola@imaa.cnr.it",
    license='ECMWF',
    url="https://github.com/emanueletramutola/icos_api.git",
    package_dir={f'{app_name}': f'lib/{app_name}'},
    packages=setuptools.find_packages('lib'),
    install_requires=[
        'pandas', 'hug', 'dacite',
        'requests', 'icoscp'
    ],
    classifiers=[
        'Development Status :: Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
        'console_scripts': [
            f'build_datacube={app_name}.utils.icos_data:build_datacube'
        ],
    }
)
