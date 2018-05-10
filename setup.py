import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pw",
    version = "0.0.1",
    author = "Alexander Scheel",
    author_email = "alexander.m.scheel@gmail.com",
    description = ("A perfectly secure world"),
    license = "GPLv3",
    keywords = "kerberos perfect-world",
    url = "https://github.com/cipherboy/perfect-world",
    packages=['pw'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)

