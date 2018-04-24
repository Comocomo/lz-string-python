from setuptools import setup

import codecs
import io
from os import path

def read(*parts):
  file_path = path.join(path.dirname(__file__), *parts)
  return codecs.open(file_path, encoding='utf-8').read()

setup(
  name='lzstring',
  version='1.0.3',
  description='lz-string for python',
  author='Geza Kovacs',
  author_email='geza0kovacs@gmail.com',
  packages=['lzstring'],
  package_dir={'lzstring': 'lzstring'},
  package_data={},
  long_description=read('README.rst'),
  url='https://github.com/gkovacs/lz-string-python',
  download_url='https://github.com/gkovacs/lz-string-python',
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.1',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    ],
    install_requires=['future>=0.14.0'],
)
