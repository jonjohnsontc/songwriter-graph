from setuptools import setup, find_packages

setup(
    name="songwriter_graph",
    version="0.3",
    url="https://github.com/jonjohnsontc/songwriter-graph",
    packages=["songwriter_graph"],
    include_package_data=True,
    install_requires=['flask']
)
