from setuptools import setup

setup(
    name="minus.py",
    version="0.1",
    packages=['minus'],
    install_requires=['simplejson', 'httplib2', 'poster>=0.8.1'],
    author = "Minus Inc.",
    author_email = "info@minus.com",
    description = "Minus.com API python library",
    url = "http://minus.com",
)
