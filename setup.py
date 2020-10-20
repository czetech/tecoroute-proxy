from os import path
from types import SimpleNamespace
from runpy import run_path

from setuptools import setup, find_packages

name = 'tecoroute-proxy'
author_email = 'petr@cze.tech'
git_url_prefix = 'https://github.com/{name}'.format(name=name)
module = SimpleNamespace(**run_path(path.join(path.dirname(__file__), name, '__about__.py')))
with open('README.rst', 'r') as f:
    readme = f.read()

# add https://setuptools.readthedocs.io/en/latest/setuptools.html#id55 (metadata, options)
setup(
    zip_safe = False,
    name = name,
    version=module.__version__,
    author=module.__author__,
    author_email=author_email,
    maintainer=module.__author__,
    maintainer_email=author_email,
    url=git_url_prefix,
    description='Python example application and code structure.',
    long_description=readme,
    download_url=git_url_prefix + '/-/archive/master/{name}-master.zip',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    platforms='posix',
    keywords=[
        'example', 'czetech', 'web', 'www', 'click', 'flask'
    ],
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'tornado'
    ],
    entry_points={
        'console_scripts': [
            '{name} = {module}.cli:run'.format(name=name, module=name)
        ]
    },
    python_requires='>=3.5',
    project_urls={
        'Bug Tracker': git_url_prefix,
        'Documentation': git_url_prefix,
        'Source Code': git_url_prefix
    }
)
