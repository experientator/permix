# setup.py
from setuptools import setup, find_packages

setup(
    name='permix',
    version='0.1.0',
    packages=find_packages(),
    # Мы убрали entry_points, так как они здесь не нужны
    # и создают путаницу.
)