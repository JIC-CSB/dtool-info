from setuptools import setup

url = ""
version = "0.1.0"
readme = open('README.rst').read()
description = \
    "Dtool plugin for accessing information from datasets and collections",

setup(
    name="dtool-info",
    packages=["dtool_info"],
    version=version,
    description=description,
    long_description=readme,
    include_package_data=True,
    author="Tjelvar Olsson",
    author_email="tjelvar.olsson@jic.ac.uk",
    url=url,
    install_requires=[],
    download_url="{}/tarball/{}".format(url, version),
    license="MIT"
)
