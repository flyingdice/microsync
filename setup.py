"""
    microsync
    ~~~~~~~~~

    Keep your microservice repositories in sync.

    :copyright: (c) 2020 Andrew Hawker.
    :license: GPLv3, see LICENSE for more details.
"""
import ast
import re

try:
    from setuptools import find_packages, setup
except ImportError:
    from distutils.core import setup


GLOBAL_REGEX = re.compile(r'(\w+)\s+=\s+(.*)')


def get_meta():
    with open('microsync/meta.py', 'r') as f:
        matches = GLOBAL_REGEX.findall(f.read())
        return dict((name.lower(), ast.literal_eval(value))
                    for (name, value) in matches)


def get_long_description():
    with open('README.md') as f:
        return f.read()


meta = get_meta()

setup(
    name=meta['name'],
    version=meta['version'],
    author=meta['author'],
    author_email=meta['author_email'],
    url=meta['url'],
    license='GPLv3',
    description=meta['tagline'],
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={'microsync': ['py.typed']},
    entry_points={'console_scripts': ['microsync=microsync.cli:run']},
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
