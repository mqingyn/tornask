from setuptools import setup, find_packages
from tornask import __version__

setup(
    name="tornask",
    version=__version__,
    description="tornask is a task manager based on tornado",
    long_description="tornask is a task manager based on tornado.",
    keywords='python tornask tornado',
    author="mqingyn",
    url="https://github.com/mqingyn/tornask",
    license="BSD",
    packages=find_packages(),
    author_email="mqingyn@gmail.com",
    requires=['tornado', 'futures'],
    scripts=[],
    include_package_data=True,
    zip_safe=True,
)
