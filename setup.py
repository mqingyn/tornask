from setuptools import setup, find_packages

setup(
    name="tornask",
    version="1.0",
    description="tornask is a task manager based on tornado",
    long_description="tornask is a task manager based on tornado.",
    keywords='python tornask tornado',
    author="mqingyn",
    url="https://github.com/mqingyn/tornask",
    license="BSD",
    packages=find_packages(),
    author_email="mqingyn@gmail.com",
    requires=['tornado'],
    scripts=[],
    include_package_data=True,
    zip_safe=True,
)
