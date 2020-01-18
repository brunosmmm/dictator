"""Setup."""

from setuptools import setup, find_packages

setup(
    name="dictator",
    version="0.1",
    packages=find_packages(),
    package_dir={"": "."},
    package_data={},
    include_package_data=True,
    install_requires=[],
    author="Bruno Morais",
    author_email="brunosmmm@gmail.com",
    description="DICTionary ConfiguraTion vAlidaTOR",
    scripts=[],
)
