#!/usr/bin/env python

from setuptools import setup


setupconf = dict(
    name="blink1lib",
    version="0.1.0",
    license="GPLv3+",
    url="https://github.com/Shura1oplot/python3-blink1lib/",
    platforms=("POSIX", ),
    author="Shura1oplot",
    author_email="s0meuser@yandex.ru",
    description="Python 3 module for blink(1)",
    # long_description="",
    keywords=("blink1", ),

    packages=("blink1lib", ),
    classifiers=(
        "Development Status :: 3 - Alpha"
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ),
)


if __name__ == "__main__":
    setup(**setupconf)
